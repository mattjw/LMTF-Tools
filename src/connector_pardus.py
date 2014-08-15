""" 
Creating meta format of a the Pardos network and writing them into text files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import sys
import argparse
def create_lists(layer, node, intra_layer, inter_layer):
    """Create all files of Meta Format
    
        Args:
            layer(str): Name of the layer list file
            node(str): Name of the node list file
            intra_layer(str): Name of the intra-layer list file
            inter_layer(str): Name of the inter-layer list file
    """
    output_layer = open('%s.txt'% layer, "w")
    output_inter_layer = open('%s.txt'% inter_layer, "w")
    output_node = open('%s.txt'% node, "w")
    s = set()
    list_layer = []
    for i in range(len(sys.argv)-2):
        new_intra = str(intra_layer) + "_" + str(i+1)
        output_intra = open('%s.txt'% new_intra, "w")
        list_intra = []
        f = open(str(sys.argv[(i+2)]), "r")
        for line in f:
            seq = line.strip().split(",")
            seq.insert(2, (i+1)) #inserting layer id
            seq.insert(3, 0) #inserting time which is 0
            seq.insert(4, 1) #inserting value which is 1
            str_intra = ' '.join(str(e) for e in seq)
            list_intra.append(str_intra)
            # adding nodes in a set to create node list file
            s.add(int(seq[0]))
            s.add(int(seq[1]))
        
        output_intra.write("\n".join(str(e) for e in list_intra))
        # creating layer list file
        seq_layer = []
        seq_layer.insert(0, i+1)
        string = str(sys.argv[(i+2)])
        lay_line = string.split(".")
        seq_layer.insert(1, lay_line[0]) # layer label 
        seq_layer.insert(2, 0) # time
        str_layer = ' '.join(str(f) for f in seq_layer)
        list_layer.append(str_layer)
    output_layer.write("\n".join(str(i) for i in list_layer))
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
        """Connector for Pardus data set""")
    parser.add_argument("network", help="network name")
    parser.add_argument("first", help="the first file")
    parser.add_argument("second", help="the second file")
    parser.add_argument("third", help="the third file")
    parser.add_argument("fourth", help="the fourth file")
    return parser.parse_args()
    
def main():
    
    args = parse_arguments()
    node = str(args.network) + "_node_list"       # giving name to node list file
    layer = str(args.network) + "_layer_list"     # giving name to layer list file
    intra_layer = str(args.network) + "_intra_layer_list"       # giving name to intra-layer list file
    inter_layer = str(args.network) + "_inter_layer_list"       # giving name to inter-layer list file
    create_lists(layer, node, intra_layer, inter_layer)
    
if __name__ == '__main__':
    main()