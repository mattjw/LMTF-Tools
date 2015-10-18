""" 
Drawing multiplex network by getting datas from database
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import sys
import MySQLdb
import math
import networkx as nx
import matplotlib.pyplot as plt

class drawing():
    G = nx.Graph()
    same_layer = []
    different_layer = []
    
    # constructor of the class
    def __init__(self, username, password, network):
        self.username = username
        self.password = password
        self.network = network
    
    # connect to database    
    def connect_to_db(self):
        try:
            return MySQLdb.connect(host = "127.0.0.1", user = self.username ,
            passwd = self.password ,  port = 3306)
        except:
            pass
        try:
            return MySQLdb.connect(host = "127.0.0.1", user = self.username ,
            passwd = self.password ,  port = 3307)
        except:
            print("unable to connect database")
    
    # select database
    def select_db(self, cursor, database):
        return cursor.execute("USE " + database)
    
    # insert layer ids into the list from the layerlist table
    def list_of_layer(self,cursor, layerlist):
        layer_list = {}
        cursor.execute("SELECT * FROM " + layerlist )
        row = cursor.fetchone()
        counter = 1
        while row is not None:
            layer_list[counter] = str(row[0])
            row = cursor.fetchone()
            counter += 1
        return layer_list
        
    # insert node ids into the list from the nodelist table
    def list_of_node(self, cursor, nodelist):
        node_list = {}
        cursor.execute("SELECT * FROM " + nodelist )
        row = cursor.fetchone()
        counter = 1
        while row is not None:
            node_list[counter] = str(row[0])
            row = cursor.fetchone()
            counter += 1
        return node_list
        
    # function for placing nodes
    def placing_nodes(self, list_of_nodes, list_of_layers, G):

        k = math.sqrt(len(list_of_nodes))   # squareroot of number of nodes  

        # to find an area for each layer n*n >= number of nodes
        if k == math.floor(k):          # checking if k is an integer
            n = int(k)                  # if k = a.0  then n = a
        else:
            n = int(k+1)                # if k = a.b  then n = a+1

        # arranging place of the nodes for each layer     
        for r in range(len(list_of_layers)):
            # the first node's place is (0,0) 
            i = 0
            j = 0
    
            for s in range(len(list_of_nodes)):
                
                p = r * n      # p defines the place of each layer
                
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
        
    def placing_edges(self, cursor, multiplex, same_layer, different_layer, G, important_node):

        # reading from the multiplex table row by row
        cursor.execute('''SELECT * FROM ''' + multiplex)
        row = cursor.fetchone()

        # placing the edges
        while row is not None:
            if int(row[0]) != int(important_node) and int(row[1]) != int(important_node):
                # giving the same name to nodes as we did while placing the nodes
                m = str(row[0]) + '_' + str(row[2])
                n = str(row[1]) + '_' + str(row[3])
                # adding edges
                G.add_edge(m , n, weight= int(row[5]))
        
                if row[2] == row[3]:
                    same_layer.append((m,n))      #storing the edges which are in the same layer
                else:
                    different_layer.append((m,n))   #storing the edges which are in different layers
            row = cursor.fetchone()


def main(arg1, arg2, arg3, arg4):
    # draw is the object of class drawing
    draw = drawing(arg1, arg2, arg3)
    
    db = draw.connect_to_db()            # connecting to databse
    cursor = db.cursor()                 # creating cursor
    
    db_name = str(arg3) + "_db"          # giving name to database
    multiplex = str(arg3) + "_multiplex"       # giving name to multiplex table
    nodelist = str(arg3) + "_node_list"       # giving name to node list table
    layerlist = str(arg3) + "_layer_list"     # giving name to layer list table
    
    # graph object
    G = draw.G
    # same layer stores  the edges which are in the same layer
    same_layer = draw.same_layer
    # different layer stores  the edges which are in different layer
    different_layer = draw.different_layer
    
    draw.select_db(cursor, db_name)
    list_of_layers = draw.list_of_layer(cursor, layerlist)
    list_of_nodes = draw.list_of_node(cursor, nodelist)
    draw.placing_nodes(list_of_nodes, list_of_layers, G)
    draw.placing_edges(cursor, multiplex, same_layer, different_layer,G, arg4)
    
    pos = nx.get_node_attributes(G, 'pos')

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=5000/(len(list_of_nodes) * len(list_of_layers)), node_color='k') 
    
    # draw the edges in the same layer
    nx.draw_networkx_edges(G,pos,edgelist=same_layer, width=0.5,  edge_color = 'c')

    # draw the edges in different layers
    nx.draw_networkx_edges(G,pos,edgelist=different_layer, width=0.5, alpha=0.5,edge_color='0.20',style='dashed')
    


    plt.axis('off')
    plt.show()
                    
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
    
    