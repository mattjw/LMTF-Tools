""" 
Creating multiplex format of a network and writing them into text file
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse

# encryption of strings
def enc(x):
    """Convert non-integer inputs to integer.
    
    Args:
        x: input to be converted
        
    Returns:
        int: The integer
    """
    ord3 = lambda p : '%.3d' % ord(p)
    try:
	x = int(x)
    except:
        pass
    if isinstance(x, str):
	return int(''.join(map(ord3, x)))
    else:
	return int(x)
		
# creating multiplex file
def create_multiplex(intra_layer, inter_layer, multiplex, layer):
    """Create Multiplex Text File
    
        Args: 
            intra_layer(str): Name of the intra-layer file
            inter_layer(str): Name of the inter-layer file
            multiplex(str): Name of the multiplex file
            layer(str): Name of the layer file
    """
    # opening layer list file to read layers
    layer_file = open('%s.txt'% layer, "r")
    # creating a list to keeps layer list lines
    layer_list = []
    # opening multiplex file to write
    multiplex_file = open('%s.txt'% multiplex, "w")
    
    # getting the number of layers
    for line1 in layer_file:
        layer_list.append(line1)
    
    # creating a list of edges for all intra-layer lists and inter-layer list
    list_of_edges = []
        
    # store all edges from all intra-layer list files
    for x in range(len(layer_list)):
        # give name to each intra-layer-list
        new_intra_layer = str(intra_layer) + "_" + str(x+1)
        # open intra-layer list file
        intra_layer_file = open('%s.txt'% new_intra_layer, "r")
        # store all lines of the intra-layer list file in a list
        for line1 in intra_layer_file:
            seq1 = line1.split()
            for j in range(3):
                seq1[j] = enc(seq1[j])
            layerid = seq1[2]
            seq1.insert(3, layerid)    # layer2 id
            if "[" in seq1[5]:
                newstr1 = seq1[5].replace("[", "")
                newstr2 = newstr1.replace("]", "")
                newstr3 = newstr2.replace("'", "")
                a = newstr3.split(",")
                seq1.pop(5)
                for k in range(len(a)):
                    seq1.append(a[k])
            str1 = ' '.join(str(e) for e in seq1)
            list_of_edges.append(str1)
        
    # opening inter-layer file
    inter_layer_file = open('%s.txt'% inter_layer, "r")
    # store all edges from inter-layer list file
    for line2 in inter_layer_file:
        seq2 = line2.split()
        for j in range(4):
            seq2[j] = enc(seq2[j])
        if "[" in seq2[5]:
            newstr1 = seq2[5].replace("[", "")
            newstr2 = newstr1.replace("]", "")
            newstr3 = newstr2.replace("'", "")
            b = newstr3.split(",")
            seq2.pop(5)
            for k in range(len(b)):
                seq2.append(b[k])
        str1 = ' '.join(str(e) for e in seq2)
        list_of_edges.append(str1)
            
    # write each list into multiplex file
    multiplex_file.write("\n".join(str(e) for e in list_of_edges))

def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Create Multiplex Format File""")
    parser.add_argument("network", help="network name") 
    
    return parser.parse_args()              
                                    
def main():
    args = parse_arguments()
    multiplex = str(args.network) + "_multiplex"       # giving name to multiplex file
    layer = str(args.network) + "_layer_list"     # giving name to layer list file
    intra_layer = str(args.network) + "_intra_layer_list"   # giving name to intra layer list file
    inter_layer = str(args.network) + "_inter_layer_list"   # giving name to inter layer list file
    # call the function to create multiplex file             
    create_multiplex(intra_layer, inter_layer, multiplex, layer)
    
if __name__ == '__main__':
    main()  