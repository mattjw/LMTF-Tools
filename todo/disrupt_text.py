""" 
Drawing multiplex network by getting datas from text file
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import sys
import math
import networkx as nx
import matplotlib.pyplot as plt

class Drawing():
    G = nx.Graph()
    same_layer = []
    different_layer = []
    
    # constructor of the class
    def __init__(self):
        pass


    # create layer list
    def list_of_layer(self,layerlist):
        layer_list = {}
        f = open('%s.txt'% layerlist, "r")
        counter = 1
        for line in f:
            seq = line.split()
            layer_list[counter] = str(seq[0])
            counter += 1
        return layer_list
    

    # create nodelist
    def list_of_node(self,nodelist):
        node_list = {}
        f = open('%s.txt'% nodelist, "r")
        counter = 1
        for line in f:
            seq = line.split()
            node_list[counter] = str(seq[0])
            counter += 1
        return node_list

    # place nodes
    def placing_nodes(self, list_of_nodes, list_of_layers, G):
        
        k = math.sqrt(len(list_of_nodes))   # squareroot of number of nodes  

        # to find an area for each layer n*n >= number of nodes
        if k == math.floor(k):          # checking if k is an integer
            n = int(k)                  # if k = a.0  then n = a
        else:
            n = int(k+1)                # if k = a.b and b>0 then n = a+1
    
        # arranging place of the nodes for each layer   
        for r in range(len(list_of_layers)):
            
            # the first node's place is (0,0)
            i = 0
            j = 0
            for s in range(len(list_of_nodes)):
            
                p = r * n             # p defines the place of each layer
            
                # each node has different name in different layers
                node = str(list_of_nodes[s+1]) + '_' + str(list_of_layers[r+1])
            
                # placing nodes starting from the first row
                if i<n:
                    G.add_node(node , pos = ((i+p), (j+p)))
                    i = i+1
                # if first row is full go the the next row
                else:
                    i = 0
                    j = j+1
                    G.add_node(node , pos = ((i+p), (j+p)))
                    i = i+1

   
   # function for drawing edges
    def placing_edges(self,multiplex, G, same_layer, different_layer, important_node):
        
        # reading from the multiplex file
        f2 = open('%s.txt'% multiplex, "r")
    
        # placing the edges
        for line4 in f2:
        
            list4 = line4.split()
            if int(list4[0]) != int(important_node) and int(list4[1]) != int(important_node):
                # giving the same name to nodes as we did while placing the nodes
                m = str(list4[0]) + '_' + str(list4[2])
                n = str(list4[1]) + '_' + str(list4[3])
                # adding edges
                G.add_edge(m , n, weight= float(list4[5]))
        
                if list4[2] == list4[3]:
                    same_layer.append((m,n))      #storing the edges which are in the same layer
                else:
                    different_layer.append((m,n))   #storing the edges which are in different layers  
                
def main(arg1, arg2):
    dr = Drawing()
    multiplex = str(arg1) + "_multiplex"       # giving name to multiplex table
    nodelist = str(arg1) + "_node_list"       # giving name to node list table
    layerlist = str(arg1) + "_layer_list"     # giving name to layer list table                  
    # list of all layers
    list_of_layers = dr.list_of_layer(layerlist)
    # list of all nodes
    list_of_nodes = dr.list_of_node(nodelist)
    # graph object
    G = dr.G
    # same layer list is for the edges where each node is in the same layer
    same_layer = dr.same_layer
    # different layer list is for the edges where each node is in different layer
    different_layer = dr.different_layer 
    # place the nodes
    dr.placing_nodes(list_of_nodes, list_of_layers, G)
    # place the edges
    dr.placing_edges(multiplex, G, same_layer, different_layer, arg2)
               
    pos = nx.get_node_attributes(G, 'pos')

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=5000/(len(list_of_nodes) * len(list_of_layers)), node_color='k') 

    # draw the edges in the same layer
    nx.draw_networkx_edges(G,pos,edgelist=same_layer, width=0.5, edge_color = 'c')

    # draw the edges in different layers
    nx.draw_networkx_edges(G,pos,edgelist=different_layer, width=0.5, alpha=0.5,edge_color='0.20',style='dashed')

    plt.axis('off')
    plt.show()
    
if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]))
    