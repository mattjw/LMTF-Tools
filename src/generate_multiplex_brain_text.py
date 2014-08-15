""" 
Creating multiplex format of the brain network and writing them into text file
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse
import generate_multiplex_text

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
    for i in range(45):
        multiplex = str(args.network) + str(i+1) +  "_multiplex"       # giving name to multiplex file
        layer = str(args.network) + str(i+1) + "_layer_list"     # giving name to layer list file
        intra_layer = str(args.network) + str(i+1) + "_intra_layer_list"   # giving name to intra layer list file
        inter_layer = str(args.network) + str(i+1) + "_inter_layer_list"   # giving name to inter layer list file
        generate_multiplex_text.create_multiplex(intra_layer, inter_layer, multiplex, layer)
        
def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Create Multiplex Format File for Brain Network""")
    parser.add_argument("network", help="network name") 
    
    return parser.parse_args()
    
def main():
    create_multiplex()
    
if __name__ == '__main__':
    main() 