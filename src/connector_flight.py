""" 
Creating meta format of a the flight network and writing them into text files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import sys

class Connector():
    # constructor of the class
    def __init__(self):
        pass
        
    # find all layers
    def find_all_layers(self, arg2):
        # define a set
        s = set()
        # define a list to store all layer ids
        layer_list = []
        # opening the file
        f = open(arg2, "r")     
        for line in f:
            l = line.split(",")
            for n, i in enumerate(l):
	       if i == '\N':
	           l[n] = None
        
            t = l[1], l[0]          # tuple countains airline id (layer) and airline name
            s.add(t)                # storing in a set not to contain the same elements
            
        # store all ids of the layers in a list
        for e in s:
            layer_list.append(e)
            
        return layer_list
        
    # find all nodes
    def find_all_nodes(self, arg2):
        # define a set
        s = set()
        # define a list to store all node ids
        node_list = []
        # open the file
        f = open(arg2, "r")     
        for line in f:
            l = line.split(",")
            # convert "\N" to None for storing into database
            for n, i in enumerate(l):
                if i == '\N':
                    l[n] = None
            # t1 countains source airport id (node) and airport name
            t1 = l[3], l[2]   
            # t2 countains destination airport id (node) and airport name
            t2 = l[5], l[4]
            # storing in a set not to contain the same elements
            s.add(t1)                
            s.add(t2)
        # store all ids of the layers in a list
        for e in s:
            node_list.append(e)
            
        return node_list
        
    """ select most popular layers (airline companies)
        and create layer_list file
    """
    def select_layers(self, all_layer_list, layer, arg2):
        #create a list to store 10 popular layers
        list_of_layers = []
        # create a list to keep each selected layer and its frequency
        list_of_frequency = []
        # create a list to keep only 10 popular layer ids
        layer_id = []
        
        for k in all_layer_list:
            # define a counter for each layer
            counter = 0
            # open the file
            f = open(arg2, "r")
            for line in f:
                l = line.split(",")
                # convert "\N" to None for storing into database
                for n, i in enumerate(l):
                    if i == '\N':
                        l[n] = None
                if l[1] != None:
                    if l[1] == k[0]:
                        counter += 1
            t = k, counter    # t contains layer and counter        
            # add the layer and its frequency in a list
            list_of_frequency.append(t)
        
        # sort the list in reverse order
        new_sorted = sorted(list_of_frequency, key = lambda tup : tup[1], reverse = True)
        
        # select 10 most popular airlines
        for i in range(10):
            x = new_sorted[i]
            list_of_layers.append(x[0])
        
        # open a file for layer list
        output_layer = open('%s.txt'% layer, "w")
        # create a layer list to keep the each line of the layers
        layer_list =[]
        
        for e in list_of_layers:
            layer_id.append(e[0])
            seq = []
            seq.append(e[0])
            seq.append(e[1])
            seq.append(0)
            string = ' '.join(str(f) for f in seq)
            layer_list.append(string)
        # write in the layer list file
        output_layer.write("\n".join(str(i) for i in layer_list))  
        return layer_id
        
    """ select most popular nodes (airports)
        and create node_list file
    """
    def select_nodes(self, all_node_list, arg2, node):
        #create a list to store 100 popular nodes
        list_of_nodes = []
        # create a list to keep each selected node and its frequency
        list_of_frequency = []
        # create a list to keep only node ids of 100 populer airports
        node_id = []
        
        for k in all_node_list:
            # define a counter for each node
            counter = 0
            # open the file
            f = open(arg2, "r")
            for line in f:
                l = line.split(",")
                # convert "\N" to None for storing into database
                for n, i in enumerate(l):
                    if i == '\N':
                        l[n] = None
                if l[3] != None and l[5] != None:
                    if l[3] == k[0] or l[5] == k[0]:
                        counter += 1
            t = k, counter    # t contains node and counter
             # add the node and its frequency in a list
            list_of_frequency.append(t) 
            
        # sort the list in reverse order
        new_sorted = sorted(list_of_frequency, key = lambda tup : tup[1], reverse = True)
        
        # select 100 most popular airports
        for i in range(100):
            x = new_sorted[i]
            list_of_nodes.append(x[0])
        
        # open a file for layer list
        output_layer = open('%s.txt'% node, "w")
        # create a layer list to keep the each line of the layers
        node_list =[]
        
        for e in list_of_nodes:
            node_id.append(e[0])
            seq = []
            seq.append(e[0])
            seq.append(0)
            seq.append(e[1])
            string = ' '.join(str(f) for f in seq)
            node_list.append(string)
        # write in the layer list file
        output_layer.write("\n".join(str(i) for i in node_list)) 
            
        return node_id
    
    # create intra-layer list files
    def create_intra_layer_list(self,intra_layer, arg2, list_of_layers, list_of_nodes):
        counter = 1
        for k in list_of_layers:
            # give a name to new intra-layer list file
            new_intra = str(intra_layer) + "_" + str(counter)
            # open a intra-layer list file for each layer
            output_intra = open('%s.txt'% new_intra, "w")
             # create a list to keep the lines of intra-layer list file
            list_of_lines = []
            f = open(arg2, "r")     #opening the file
            for line in f:
                l = line.split(",")
                # convert "\N" to None for storing into database
                for n, i in enumerate(l):
                    if i == '\N':
                        l[n] = None
                if l[1] == k:
                    if l[3] != None and l[5] != None:
                        if l[3] in list_of_nodes and l[5] in list_of_nodes:
                            seq = []
                            seq.append(l[3])
                            seq.append(l[5])
                            seq.append(k)
                            seq.append(0)
                            seq.append(int(l[7])+1)
                            # joining the elements of the sequence and store the line in a list
                            string = ' '.join(str(e) for e in seq)
                            list_of_lines.append(string)
            # write in the intra-list file
            output_intra.write("\n".join(str(e) for e in list_of_lines))
            counter += 1
            
    # create inter-layer list file
    def create_inter_layer_list(self, inter_layer):
        # open a file to write node list
        open('%s.txt'% inter_layer, "w")
        

def main(arg1, arg2):
    # c is the object of class Connector
    c = Connector()

    intra_layer = str(sys.argv[1]) + "_intra_layer_list"       # giving name to intra-layer list file
    inter_layer = str(sys.argv[1]) + "_inter_layer_list"       # giving name to inter-layer list file
    node = str(sys.argv[1]) + "_node_list"       # giving name to node list file
    layer = str(sys.argv[1]) + "_layer_list"     # giving name to layer list file
    
    all_layer_list = c.find_all_layers(arg2)
    all_node_list = c.find_all_nodes(arg2)
    
    list_of_layers = c.select_layers(all_layer_list, layer, arg2)
    list_of_nodes = c.select_nodes(all_node_list, arg2, node)
    
    c.create_intra_layer_list(intra_layer, arg2, list_of_layers, list_of_nodes)
    c.create_inter_layer_list(inter_layer)

if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]))     