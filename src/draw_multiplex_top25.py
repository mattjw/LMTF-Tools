""" 
Drawing multiplex network by getting datas from text file
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse
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
        """Insert Layer ids into a Dictionary
        
        Args:
            layerlist (str): The name of the layer list file
            
        Returns:
            dict: The dictionary
        
        """
        layer_list = {}
        f = open('%s.txt'% layerlist, "r")
        counter = 1
        for line in f:
            seq = line.split()
            layer_list[counter] = str(seq[0])
            counter += 1
        return layer_list
    

    # create nodelist
    def list_of_node(self,nodelist, multiplex):
        """Insert Node ids into a list
        
        Args:
            nodelist (str): The name of the node list file
            
        Returns:
            list: The list of node ids 
        """
        list_node = []   # list of all nodes
        list_frequency = []   # list of all nodes and their frequency
        nodes = []    # list of top 25 nodes
        f = open('%s.txt'% nodelist, "r")
        for line in f:
            seq = line.split()
            list_node.append(seq[0])
        
        for i in list_node:
            counter = 0
            g = open('%s.txt'% multiplex, "r")
            for line in g:
                s = line.split()
                if s[0] == i or s[1] == i:
                    counter += 1
            t = i, counter
            list_frequency.append(t)
        new_sorted = sorted(list_frequency, key = lambda tup : tup[1], reverse = True)
        #print new_sorted
        for i in range(25):
            x = new_sorted[i]
            nodes.append(x[0])
        
        return nodes

    # place nodes
    def placing_nodes(self, nodes, layers, G):
        """Place the nodes of each layer
        
        Args:
            nodes(list): List of node ids
            layer(dict): Dictionary of layer ids
            G(Graph): A Graph object
        """
        k = math.sqrt(len(nodes))   # squareroot of number of nodes  

        # to find an area for each layer n*n >= number of nodes
        if k == math.floor(k):          # checking if k is an integer
            n = int(k)                  # if k = a.0  then n = a
        else:
            n = int(k+1)                # if k = a.b and b>0 then n = a+1
    
        # arranging place of the nodes for each layer   
        for r in range(len(layers)):
            
            # the first node's place is (0,0)
            i = 0
            j = 0
            for s in nodes:
            
                p = r * n             # p defines the place of each layer
            
                # each node has different name in different layers
                node = str(s) + '_' + str(layers[r+1])
            
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
    def placing_edges(self,multiplex, G, same_layer, different_layer, nodes):
        """Place the edges between nodes
        
        Args:
           multiplex(str): Name of the multiplex table
           G(Graph): A Graph object
           same_layer(list): List of edges which are in same layer
           different_layer(list): List of edges which are in different layer
           nodes(list): List of node ids            
        """
        
        f = open('%s.txt'% multiplex, "r")
        
        for line4 in f:
        
            list4 = line4.split()
            if list4[0] in nodes and list4[1] in nodes:
                # giving the same name to nodes as we did while placing the nodes
                m = str(list4[0]) + '_' + str(list4[2])
                n = str(list4[1]) + '_' + str(list4[3])

                G.add_edge(m , n, weight= 1)
        
                if list4[2] == list4[3]:
                    same_layer.append((m,n))      #storing the edges which are in the same layer
                else:
                    different_layer.append((m,n))   #storing the edges which are in different layers  

def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Draw Multiplex Network""")
    parser.add_argument("network", help="network name") 
    
    return parser.parse_args()                 
                                                
def main():
    args = parse_arguments()
    dr = Drawing()
    multiplex = str(args.network) + "_multiplex"       # giving name to multiplex table
    nodelist = str(args.network) + "_node_list"       # giving name to node list table
    layerlist = str(args.network) + "_layer_list"     # giving name to layer list table                  
    # list of all layers
    list_of_layers = dr.list_of_layer(layerlist)
    # list of all nodes
    list_of_nodes = dr.list_of_node(nodelist, multiplex)
    # graph object
    G = dr.G
    # same layer list is for the edges where each node is in the same layer
    same_layer = dr.same_layer
    # different layer list is for the edges where each node is in different layer
    different_layer = dr.different_layer 
    # place the nodes
    dr.placing_nodes(list_of_nodes, list_of_layers, G)
    # place the edges
    dr.placing_edges(multiplex, G, same_layer, different_layer, list_of_nodes)
               
    pos = nx.get_node_attributes(G, 'pos')

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000/(len(list_of_nodes) * len(list_of_layers)), node_color='k') 

    # draw the edges in the same layer
    nx.draw_networkx_edges(G,pos,edgelist=same_layer, width=0.5, edge_color = 'c')

    # draw the edges in different layers
    nx.draw_networkx_edges(G,pos,edgelist=different_layer, width=0.5, alpha=0.5,edge_color='0.20',style='dashed')

    plt.axis('off')
    plt.show()
    
if __name__ == '__main__':
    main()
    