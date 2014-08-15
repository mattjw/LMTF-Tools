""" 
Creating multiplex format of the brain network and storing meta and multiplex format into database
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse
import generate_multiplex_db

# creating multiplex file
def create_multiplex():
    """Create Multiplex Text File
    
        Args: 
            intra_layer(str): Name of the intra-layer file
            inter_layer(str): Name of the inter-layer file
            multiplex(str): Name of the multiplex file
            layer(str): Name of the layer file
    """
    args = parse_arguments()
    m = generate_multiplex_db.Multiplex()
    db = m.connect_to_db(args.username,args.password)            # connecting to databse
    cursor = db.cursor()                 # creating cursor
    for i in range(45):
        multiplex = str(args.network) + str(i+1) +  "_multiplex"       # name of multiplex file
        layer = str(args.network) + str(i+1) + "_layer_list"     # name of layer list file
        intra_layer = str(args.network) + str(i+1) + "_intra_layer_list"   # name of intra layer list file
        inter_layer = str(args.network) + str(i+1) + "_inter_layer_list"   # name of inter layer list file
        node = str(args.network) + str(i+1) + "_node_list"     # name of node list file
        db_name = str(args.network) + str(i+1) + "_db"     # name of database
        
        m.create_db(cursor, db_name)
        layer_list = m.create_layer_list(cursor, layer)
        m.create_node_list(cursor, node)
        m.create_inter_layer_list(cursor, inter_layer)
        m.create_intra_layer_lists( cursor, intra_layer, layer_list)
        m.create_multiplex(cursor, multiplex, intra_layer, inter_layer, layer_list)
        
        
def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Create Multiplex Format and Store in the MySQL Database""")
    parser.add_argument("username", help="username")
    parser.add_argument("password", help="password")
    parser.add_argument("network", help="network name") 
    
    return parser.parse_args() 
    
def main():
    create_multiplex()
    
if __name__ == '__main__':
    main() 