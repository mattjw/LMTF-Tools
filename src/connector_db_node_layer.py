""" 
Creating meta format of a data set stored in a MySQL database and writing them into text files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>
import argparse
import MySQLdb

class DatabaseConnector():
    
    def __init__(self, username, password, dbName):
        self.username = username
        self.password = password
        self.dbName = dbName
        
    # connection to database
    def connect_to_db(self):
        """Connect to MySQL database"""
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
    def select_db(self, cr):
        """Select the database
        
        Args:
            cr (cursor): Cursor to execute the SQL statement
            
        """
        cr.execute("USE " + self.dbName)
    
    # encryption of strings
    def enc(self, x):
        """Convert non-integer inputs to integer.
        
        Args:
            x: input to be converted
            
        Returns:
            int: The integer
        """
	ord3 = lambda p : '%.3d' % ord(p)
	try:
	    x = int(x)
	except:
	    pass
	if isinstance(x, str):
		return int(''.join(map(ord3, x)))
	else:
		return int(x)
		    
    # create layerlist  and nodelist file
    def layer_and_node_list(self, cr, nc1, v1, nc2, v2, layer, node, table):
        """Create layer list file and node list file and return list of id values of layers
        
        Args:
            cr (cursor): Cursor to execute the SQL statement
            nc1 (int): The column number of the first node
            v1 (int): The column number of the first node's value
            nc2 (int): The column number of the second node
            v2 (int): The column number of the second node's value
            layer (str): The name of the layer list file
            node (str): The name of the node list file
            table (str): Name of the tables storing each layer
            
        Returns:
            list: The list of layer ids
        
        """
        output_layer = open('%s.txt'% layer, "w")
        output_node = open('%s.txt'% node, "w")
        s_node = set()
        for e in table:
            cr.execute("SELECT * FROM " + e)
            row = cr.fetchone()
            while row is not None:
                tuple_n1 = self.enc(row[nc1]), row[v1]
                s_node.add(tuple_n1)
                tuple_n2 = self.enc(row[nc2]), row[v2]
                s_node.add(tuple_n2)
                row = cr.fetchone()
        
        nodelist = []
        sorted_s_node = sorted(s_node, key=lambda tup: tup[0])
        for e in sorted_s_node:
            seq = []
            seq.append(e[0])
            seq.append(0)
            seq.append(e[1])
            string_node = ' '.join(str(f) for f in seq)
            nodelist.append(string_node)
        # write in the node list file
        output_node.write("\n".join(str(i) for i in nodelist))
        
def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Create Meta Format by Getting Data from Database""")
    parser.add_argument("username", help="username")
    parser.add_argument("password", help="password")
    parser.add_argument("network", help="network name")
    parser.add_argument("dbName", help="database name")
    parser.add_argument("nc1", type = int, 
        help="the first node column (ie. 0,1,2...)")
    parser.add_argument("v1", type = int, 
        help="column number of the value of the first node. If not available, write the first node column (ie. 0,1,2...)")
    parser.add_argument("nc2", type = int, 
        help="the second node column (ie. 0,1,2...)")
    parser.add_argument("v2", type = int, 
        help="column number of the value of the second node. If not available, write the second node column (ie. 0,1,2...)")
    parser.add_argument('tableName', metavar='N', type=str, nargs='*', 
        help="Name of the tables storing each layer")
    
    return parser.parse_args()
    
def main():
    args = parse_arguments()
    # c is the object of class DatabaseConnector
    c = DatabaseConnector(args.username, args.password, args.dbName)
    node = str(args.network) + "_node_list"       # giving name to node list file
    layer = str(args.network) + "_layer_list"     # giving name to layer list file
    
    db = c.connect_to_db()
    cr = db.cursor()
    c.select_db(cr)
    c.layer_and_node_list(cr, args.nc1, args.v1, args.nc2, args.v2, layer, node, args.tableName)
    
if __name__ == '__main__':
    main()