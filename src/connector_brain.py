""" 
Creating meta format of a the Brain network and writing them into text files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse

def create_lists(f, a):
    """Create all files of Meta Format
    
        Args:
            f(str): Name of the functional layer file
            a(str): Name of the anatomical layer file
    """
    s = set()
    list_intra2 = []
    args = parse_arguments()
    file_DTI = open(a, "r")
    for line in file_DTI:
        sq = line.strip().split("\t")
        sq.insert(2, 2) # inserting layer number which is 2 for anatomical layer
        sq.insert(3, 0) # inserting time variable which is 0
        str_intra2 = ' '.join(str(e) for e in sq)
        list_intra2.append(str_intra2)
        # adding nodes in a set to create node list file
        s.add(int(sq[0]))
        s.add(int(sq[1]))
    
    for i in range(45):
        node = str(args.network) + str(i+1)+ "_node_list"       # giving name to node list file
        layer = str(args.network) +str(i+1)+ "_layer_list"     # giving name to layer list file
        intra_layer = str(args.network) +str(i+1)+ "_intra_layer_list"       # giving name to intra-layer list file
        inter_layer = str(args.network) +str(i+1)+ "_inter_layer_list"       # giving name to inter-layer list file
        
        output_layer = open('%s.txt'% layer, "w")
        output_inter_layer = open('%s.txt'% inter_layer, "w")
        output_node = open('%s.txt'% node, "w")
        
        subj = f.split("_")
        subj[2] = str(i+1)
        func = '_'.join(str(e) for e in subj)
        # open the each functional file
        file_func = open(func, "r")
        
        
        intra1 = str(intra_layer) + "_1"
        output_intra1 = open('%s.txt'% intra1, "w")
        
        intra2 = str(intra_layer) + "_2"
        output_intra2 = open('%s.txt'% intra2, "w")
        
        
        list_intra1 = []
        for line in file_func:
            seq = line.strip().split("\t")
            seq.insert(2, 1) #inserting layer id
            seq.insert(3, 0) #inserting time which is 0
            str_intra1 = ' '.join(str(e) for e in seq)
            list_intra1.append(str_intra1)
            # adding nodes in a set to create node list file
            s.add(int(seq[0]))
            s.add(int(seq[1]))
        output_intra1.write("\n".join(str(e) for e in list_intra1))
        output_intra2.write("\n".join(str(d) for d in list_intra2))
        
        # creating layer list file
        list_layer =[]
        # for layer 1
        layer1 = []
        layer1.insert(0, 1)  # layer id
        line1 = func.split(".")
        layer1.insert(1, line1[0]) # layer label 
        layer1.insert(2, 0) # time
        str_layer1 = ' '.join(str(f) for f in layer1)
        list_layer.append(str_layer1)
        # for layer 2
        layer2 = []
        layer2.insert(0, 2)  #layer id
        line2 = a.split(".")
        layer2.insert(1, line2[0]) # layer label 
        layer2.insert(2, 0) # time
        str_layer2 = ' '.join(str(f) for f in layer2)
        list_layer.append(str_layer2)
        
        output_layer.write("\n".join(str(i) for i in list_layer))
        # node list file
        list_node = []
        sort = sorted(s) 
        for x in sort:
            n = []
            n.insert(0, x)
            n.insert(1, 0) #timestamp
            n.insert(2, 1) #value
            str_node = ' '.join(str(f) for f in n)
            list_node.append(str_node)
        output_node.write("\n".join(str(i) for i in list_node))
        
            
        
def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Connector for Brain data set""")
    parser.add_argument("network", help="network name")
    parser.add_argument("functional", help="one of the functional file")
    parser.add_argument("anatomical", help="anatomical file")
    return parser.parse_args()
    
def main():
    args = parse_arguments()
    f = str(args.functional)
    a = str(args.anatomical)
    create_lists(f, a)

if __name__ == '__main__':
    main()           