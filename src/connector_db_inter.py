""" 
Creating meta format of a data set stored in a MySQL database and writing them into text files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>
import argparse
import MySQLdb

class DatabaseConnector():
    
    def __init__(self, username, password, dbName, tableName):
        self.username = username
        self.password = password
        self.dbName = dbName
        self.tableName = tableName
        
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
		    
            
    def inter_layer_list(self, cr, inter_layer, lc1, lc2, nc1, nc2, v):
        """Create inter layer list file
        
        Args:
            cr (cursor): Cursor to execute the SQL statement
            inter_layer (str): The name of the inter-layer list file
            lc1 (int): The column number of the first layer
            lc2 (int): The column number of the second layer
            nc1 (int): The column number of the first node
            nc2 (int): The column number of the second node
            v (int): The column number of the value of the given relation
        
        """
        output_inter = open('%s.txt'% inter_layer, "w")
        inter_list = []
        cr.execute("SELECT * FROM " + self.tableName)
        row = cr.fetchone()
        while row is not None:
            if row[lc1] != row[lc2]:
                seq = []
                seq.append(self.enc(row[nc1]))
                seq.append(self.enc(row[nc2]))
                seq.append(self.enc(row[lc1]))
                seq.append(self.enc(row[lc2]))
                seq.append(0)
                for e in v:
                    seq.append(row[e])
                # joining the elements of the sequence and store the line in a list
                string = ' '.join(str(e) for e in seq)
                inter_list.append(string)
            row = cr.fetchone()
        # write in the inter-list file
        output_inter.write("\n".join(str(e) for e in inter_list))
        
def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Create Meta Format by Getting Data from Database""")
    parser.add_argument("username", help="username")
    parser.add_argument("password", help="password")
    parser.add_argument("network", help="network name")
    parser.add_argument("dbName", help="database name")
    parser.add_argument("tableName", help="table name")
    parser.add_argument("lc1", type = int, 
        help="the first layer column (ie. 0,1,2...)")
    parser.add_argument("lc2", type = int, 
        help="the second layer column. If not available, write the first layer column (ie. 0,1,2...)")
    parser.add_argument("nc1", type = int, 
        help="the first node column (ie. 0,1,2...)")
    parser.add_argument("nc2", type = int, 
        help="the second node column (ie. 0,1,2...)")
    parser.add_argument('v', metavar='N', type=int, nargs='*', 
        help="if it exists, column number (or numbers) of the value of the given relation.(ie. 0,1,2...).")
    
    return parser.parse_args()
    
def main():
    args = parse_arguments()
    # c is the object of class DatabaseConnector
    c = DatabaseConnector(args.username, args.password, args.dbName, args.tableName)
    
    inter_layer = str(args.network) + "_inter_layer_list"       # giving name to inter-layer list file
    
    db = c.connect_to_db()
    cr = db.cursor()
    c.select_db(cr)
    c.inter_layer_list(cr, inter_layer, args.lc1, args.lc2, args.nc1, args.nc2, args.v)
    
if __name__ == '__main__':
    main()