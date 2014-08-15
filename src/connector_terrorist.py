""" 
Creating meta format of a the terrorist network and writing them into text files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import sys

class Connector():
    # constructor of the class
    def __init__(self):
        pass
        
    def create_intra_layer_and_layer_list(self, intra_layer, layer):
        # open a file for layer list
        output_layer = open('%s.txt'% layer, "w")
        # create a list to keep lines for layer list
        list_of_layers = []
        for j in range(len(sys.argv)-2):
            # give a name to new intra-layer list file
            new_intra = str(intra_layer) + "_" + str(j+1)
            # open a intra-layer list file for each layer
            output_intra = open('%s.txt'% new_intra, "w")
            # create a list to keep the lines of intra-layer list file
            list_of_lines = []
            f = open(str(sys.argv[(j+2)]), "r")     #opening the file
            line = f.next()
            list = line.split()
            N = int(list[1])  # N gives the number of nodes
    
            # reading until line (N+1)
            for i in xrange((N+1)):
                f.next()
            # reading after line (N+1)
            for l in f:
                seq = l.split()
                seq.insert(2, (j+1)) #inserting layer id
                seq.insert(3, 0) #inserting time which is 0
                # joining the elements of the sequence and store the line in a list
                str1 = ' '.join(str(e) for e in seq)
                list_of_lines.append(str1)
            # write in the intra-list file
            output_intra.write("\n".join(str(e) for e in list_of_lines))
            
            # inserting layer id, label and time into layerlist file
            lay = []
            lay.insert(0, (j+1))
            string = str(sys.argv[(j+2)])
            lay_line = string.split(".")
            lay.insert(1, lay_line[0])
            lay.insert(2, 0)
            # joining the elements of the sequence and store the line in a list
            str2 = ' '.join(str(f) for f in lay)
            list_of_layers.append(str2)
        # write in the layer list file
        output_layer.write("\n".join(str(i) for i in list_of_layers))
        
    # creates node list file
    def create_node_list(self, node):
        # open a file to write node list
        output_node = open('%s.txt'% node, "w")
        # create a list to keep lines for node list
        list_of_nodes = []
        g = open(str(sys.argv[(2)]), "r")     #opening the file
        line = g.next()
        list1 = line.split()
        N = int(list1[1])
        counter = 0
        # inserting nodes into nodelist file
        while counter < N:
            li = g.next()
            sequence = li.split()
            # create another list to store only node id, time and value
            newSeq = []
            newSeq.append(sequence[0]) # nodeid
            newSeq.append(0)   # time
            newSeq.append(1)   # value
            str3 = ' '.join(str(e) for e in newSeq)
            list_of_nodes.append(str3) 
            counter += 1
        # write in the layer list file
        output_node.write("\n".join(str(i) for i in list_of_nodes))
        
    # creates inter-layer list file
    def create_inter_layer_list(self, inter_layer):
        # open a file to write node list
        open('%s.txt'% inter_layer, "w")
        
def main(*args):
    
    # c is the object of class Connector
    c = Connector()

    intra_layer = str(sys.argv[1]) + "_intra_layer_list"       # giving name to intra-layer list file
    inter_layer = str(sys.argv[1]) + "_inter_layer_list"       # giving name to inter-layer list file
    node = str(sys.argv[1]) + "_node_list"       # giving name to node list file
    layer = str(sys.argv[1]) + "_layer_list"     # giving name to layer list file
    
    c.create_intra_layer_and_layer_list(intra_layer, layer)
    c.create_node_list(node)
    c.create_inter_layer_list(inter_layer)
    
if __name__ == '__main__':
    main()  