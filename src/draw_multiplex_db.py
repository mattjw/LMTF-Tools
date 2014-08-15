""" 
Drawing multiplex network by getting datas from database
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse
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
        """Create Connection to MySQL Database"""
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
    def select_db(self, cr, database):
        """Select the Database
            
            Args:
            cr (cursor): Cursor to execute the SQL statement
            database(str): Name of the database
            
        """
        cr.execute("USE " + database)
    
    # insert layer ids into a dictionary from the layerlist table
    def list_of_layer(self,cr, layerlist):
        """Insert Layer ids into a Dictionary
        
            Args:
                cr(cursor): Cursor to execute the SQL statement
                layerlist(str): Name of the layer list table
                
            Returns:
                dict: dictionary of layer ids
        """
        layer_list = {}
        cr.execute("SELECT * FROM " + layerlist )
        row = cr.fetchone()
        counter = 1
        while row is not None:
            layer_list[counter] = str(row[0])
            row = cr.fetchone()
            counter += 1
        return layer_list
        
    # insert node ids into the dictionary from the nodelist table
    def list_of_node(self, cr, nodelist):
        """Insert Node ids into a Dictionary 
        
            Args:
                cr(cursor): Cursor to execute the SQL statement
                nodelist(str): Name of the node list table
                
            Returns:
                dict: dictionary of node ids
        """
        node_list = {}
        cr.execute("SELECT * FROM " + nodelist )
        row = cr.fetchone()
        counter = 1
        while row is not None:
            node_list[counter]= str(row[0])
            row = cr.fetchone()
            counter += 1
        return node_list
        
    # function for placing nodes
    def placing_nodes(self, nodes, layers, G):
        """Place the nodes of each layer
        
            Args:
                nodes(dict): Dictionary of node ids
                layer(dict): Dictionary of layer ids
                G(Graph): A Graph object
        """
        k = math.sqrt(len(nodes))   # squareroot of number of nodes  

        # to find an area for each layer n*n >= number of nodes
        if k == math.floor(k):          # checking if k is an integer
            n = int(k)                  # if k = a.0  then n = a
        else:
            n = int(k+1)                # if k = a.b  then n = a+1

        # arranging place of the nodes for each layer     
        for r in range(len(layers)):
            # the first node's place is (0,0) 
            i = 0
            j = 0
    
            for s in range(len(nodes)):
        
                p = r * n      # p defines the place of each layer
        
                # each node has different name in different layers
                node = str(nodes[s+1]) + '_' + str(layers[r+1])
        
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
        
    def placing_edges(self, cr, multiplex, same_layer, different_layer, G):
        """Place the edges between nodes
        
            Args:
               cr (cursor): Cursor to execute the SQL statement
               multiplex(str): Name of the multiplex table
               same_layer(list): List of edges which are in same layer
               different_layer(list): List of edges which are in different layer
               G(Graph): A Graph object 
        """

        cr.execute('''SELECT * FROM ''' + multiplex)
        row = cr.fetchone()

        while row is not None:
            # giving the same name to nodes as we did while placing the nodes
            m = str(row[0]) + '_' + str(row[2])
            n = str(row[1]) + '_' + str(row[3])

            G.add_edge(m , n, weight= 1)
        
            if row[2] == row[3]:
                same_layer.append((m,n))      #storing the edges which are in the same layer
            else:
                different_layer.append((m,n))   #storing the edges which are in different layers
            row = cr.fetchone()

def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Draw Multiplex Network""")
    parser.add_argument("username", help="username")
    parser.add_argument("password", help="password")
    parser.add_argument("network", help="network name") 
    
    return parser.parse_args() 

def main():
    args = parse_arguments()
    # draw is the object of class drawing
    draw = drawing(args.username, args.password, args.network)
    
    db = draw.connect_to_db()            # connecting to databse
    cursor = db.cursor()                 # creating cursor
    
    db_name = str(args.network) + "_db"          # giving name to database
    multiplex = str(args.network) + "_multiplex"       # giving name to multiplex table
    nodelist = str(args.network) + "_node_list"       # giving name to node list table
    layerlist = str(args.network) + "_layer_list"     # giving name to layer list table
    
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
    draw.placing_edges(cursor, multiplex, same_layer, different_layer,G)
    
    pos = nx.get_node_attributes(G, 'pos')

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000/(len(list_of_nodes) * len(list_of_layers)), node_color='k') 
    
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
    main()
    
    