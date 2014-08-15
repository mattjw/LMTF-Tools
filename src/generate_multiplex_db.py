""" 
Creating multiplex format of a network and storing them into database
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import argparse
import MySQLdb
class Multiplex():
    
    # constructor of the class
    def __init__(self):
        pass
    
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
		
    # creates connection to database
    def connect_to_db(self, username, password):
        """Connect to MySQL database
            
            Args:
                username(str): username of the MySQL database
                password(str): password of the MySQL database
        """
        try:
            return MySQLdb.connect(host = "127.0.0.1", user = username , passwd = password ,  port = 3306)
        except:
            pass
        try:
            return MySQLdb.connect(host = "127.0.0.1", user = username , passwd = password ,  port = 3307)
        except:
            print("unable to connect database")
    # create database
    def create_db(self, cr, db_name):
        """Create a New Database
        
            Args:
                cr(cursor): Cursor to execute the SQL statement
                db_name(str): The database name to store the multiplex network
                
        """
        # create the database
        cr.execute("CREATE DATABASE " + db_name)
        # use the database
        cr.execute("USE " + db_name)
    
    # create layer list table
    def create_layer_list(self, cr, layer):
        """Create Layer List Table and insert values
        
            Args:
                cr(cursor): Cursor to execute the SQL statements
                layer(str): Name of the layer list table
                
            Returns:
                list: list of layer ids
        """
        # creating layer list table
        cr.execute(''' CREATE TABLE ''' + layer + '''(
            layerid INT,
            label VARCHAR(100),
            time TIME  
            )
            ''')
        # creating a list to keep the layerids
        layer_list = []
        
        # open the layer list file
        layer_file = open('%s.txt'% layer, "r")
        for line in layer_file:
            seq = line.split()
            seq[0] = self.enc(seq[0])
            layer_list.append(seq[0])
            # inserting layer id, label and time into layer list table
            cr.execute(''' INSERT INTO ''' + layer +''' VALUES(%s, %s, %s)''' ,
            (seq[0], seq[1], seq[2]))
            
        return layer_list
        
    # create node list table
    def create_node_list(self, cr, node):
        """Create Node List Table and insert values
            Args:
                cr(cursor): Cursor to execute the SQL statements
                node(str): Name of the node list table
        
        """
        # creates node list table
        cr.execute(''' CREATE TABLE ''' + node + '''(
            nodeid INT, 
            time TIME,
            value VARCHAR(100)  
            )
            ''')
        # open the node list file
        node_file = open('%s.txt'% node, "r")
        for line in node_file:
            seq = line.split()
            seq[0] = self.enc(seq[0])
            # inserting node id, time and value into node list table
            cr.execute(''' INSERT INTO ''' + node +''' VALUES(%s, %s, %s)''' ,
            (seq[0], seq[1], seq[2]))
    
    # creates inter-layer list table
    def create_inter_layer_list(self, cr, inter_layer):
        """Create Inter-Layer List Table and insert values
            
            Args:
                cr(cursor): Cursor to execute the SQL statements
                inter_layer(str): Name of the inter-layer list table
        
        """
        l = []   # list for the lenght of each line
        f = open('%s.txt'% inter_layer, "r")
        for line in f:
            s = line.split()
            l.append(len(s))
        try:
            max_length = max(l)        # max number of elements in a line
        except:
            max_length = 0
        
        # creates inter-layer list table without value
        cr.execute(''' CREATE TABLE ''' + inter_layer + '''(
            node1 INT ,
            node2 INT ,
            layer1 INT,
            layer2 INT, 
            time TIME,
            id INT  
            )
            ''')
        for i in range(max_length - 5):
            value = "value" + str(i+1)
            cr.execute("ALTER TABLE " + inter_layer + " ADD " + value + " VARCHAR(60)")
        
        # open the inter-layer list file
        inter_layer_file = open('%s.txt'% inter_layer, "r")
        c = 1
        for line in inter_layer_file:
            seq = line.split()
            for j in range(4):
                seq[j] = self.enc(seq[j])
            # inserting node ids, layer ids,time and value into inter-layer list table
            cr.execute(" INSERT INTO " + inter_layer +"(node1, node2, layer1, layer2, time, id) VALUES(%s, %s, %s, %s, %s, %s)" ,
            (seq[0], seq[1], seq[2], seq[3], seq[4], c))
            for i in range(max_length - 5):
                value = "value" + str(i+1)
                try:
                    cr.execute("UPDATE " + inter_layer + " SET " + value + "= %s WHERE id = %s" , (seq[i+5], c))
                except:
                    cr.execute("UPDATE " + inter_layer + " SET " + value + "= %s WHERE id = %s" , (None, c))
                    print "Error: Line " + str(c) + " in " + inter_layer + " file there is a missing value variable"
            c += 1
        # deleting the id column
        cr.execute("ALTER TABLE " + inter_layer + " DROP COLUMN id ")
        
    # creates intra-layer list tables
    def create_intra_layer_lists(self, cr, intra_layer, layer_list):
        """Create Intra-Layer List Table and insert values
        
            Args:
                cr(cursor): Cursor to execute the SQL statements
                intra_layer(str): Name of the intra-layer list table
                layer_list(list): List of layer ids
        """
        # creates intra-layer list tables
        for i in range(len(layer_list)):
            # give name to each intra-layer-list
            new_intra_layer = str(intra_layer) + "_" + str(i+1)
            l = []   # list for the lenght of each line
            f = open('%s.txt'% new_intra_layer, "r")
            for line in f:
                s = line.split()
                l.append(len(s))
            try:
                max_length = max(l)        # max number of elements in a line
            except:
                max_length = 0
            # creates a new intra-layer table for each layer
            cr.execute(''' CREATE TABLE ''' + new_intra_layer + '''(
            node1 INT ,
            node2 INT ,
            layer INT, 
            time TIME, 
            id INT  
            )
            ''')
            for i in range(max_length - 4):
                value = "value" + str(i+1)
                cr.execute("ALTER TABLE " + new_intra_layer + " ADD " + value + " VARCHAR(60)")
            # open intra-layer list file
            intra_layer_file = open('%s.txt'% new_intra_layer, "r")
            c = 1
            for line in intra_layer_file:
                seq = line.split()
                for j in range(3):
                    seq[j] = self.enc(seq[j])
                # inserting node ids, layerid, time and value into intra-layer list table
                cr.execute(''' INSERT INTO ''' + new_intra_layer +'''(node1, node2, layer, time, id) VALUES(%s, %s, %s, %s, %s)''' ,
                (seq[0], seq[1], seq[2], seq[3], c))
                for i in range(max_length - 4):
                    value = "value" + str(i+1)
                    try:
                        cr.execute("UPDATE " + new_intra_layer + " SET " + value + "= %s WHERE id = %s" , (seq[i+4], c))
                    except:
                        cr.execute("UPDATE " + new_intra_layer + " SET " + value + "= %s WHERE id = %s" , (None, c))
                        print "Error: Line " + str(c) + " in " + new_intra_layer + " file there is a missing value variable"    
                c += 1
                
            # deleting the id column
            cr.execute("ALTER TABLE " + new_intra_layer + " DROP COLUMN id ")
                
    # creates multiplex table
    def create_multiplex(self, cr, multiplex, intra_layer, inter_layer, layer_list):
        """Create Multiplex Table and Combines Intra and Inter Layer List tables
        
            Args:
                cr(cursor): Cursor to execute the SQL statements
                multiplex(str): Name of the multiplex table
                intra_layer(str): Name of the intra-layer list table
                inter_layer(str): Name of the inter-layer list table
                layer_list(list): List of layer ids
        """
        # creates multiplex table
        cr.execute("CREATE TABLE " + multiplex + '''(
            node1 INT ,
            node2 INT ,
            layer1 INT,
            layer2 INT, 
            time TIME, 
            id INT  
            )
            ''')
        l = []   # list for the lenght of each line
        for x in range(len(layer_list)):
            new_intra_layer = str(intra_layer) + "_" + str(x+1)
            f = open('%s.txt'% new_intra_layer, "r")
            for line in f:
                s = line.split()
                if "[" in s[4]:
                    newstr1 = s[4].replace("[", "")
                    newstr2 = newstr1.replace("]", "")
                    newstr3 = newstr2.replace("'", "")
                    a = newstr3.split(",")
                    s.pop(4)
                    for k in range(len(a)):
                        s.append(a[k])
                l.append(len(s)+1)
        g = open('%s.txt'% inter_layer, "r")
        for line in g:
            s = line.split()
            if "[" in s[5]:
                newstr1 = s[5].replace("[", "")
                newstr2 = newstr1.replace("]", "")
                newstr3 = newstr2.replace("'", "")
                b = newstr3.split(",")
                s.pop(5)
                for k in range(len(b)):
                    s.append(b[k])
            l.append(len(s))
        try:
            max_length = max(l)        # max number of elements in a line
        except:
            max_length = 0
        for i in range(max_length - 5):
            value = "value" + str(i+1)
            cr.execute("ALTER TABLE " + multiplex + " ADD " + value + " VARCHAR(60)")
        
        c = 1    
        # store all edges from all intra-layer list files
        for x in range(len(layer_list)):
            # give name to each intra-layer-list
            new_intra_layer = str(intra_layer) + "_" + str(x+1)
            # open intra-layer list file
            intra_layer_file = open('%s.txt'% new_intra_layer, "r")
            # store all lines of the intra-layer list file in a list
            for line1 in intra_layer_file:
                seq1 = line1.split()
                for j in range(3):
                    seq1[j] = self.enc(seq1[j])
                layerid = seq1[2]
                seq1.insert(3, layerid)    #layer2 id
                if "[" in seq1[5]:
                    newstr1 = seq1[5].replace("[", "")
                    newstr2 = newstr1.replace("]", "")
                    newstr3 = newstr2.replace("'", "")
                    a = newstr3.split(",")
                    seq1.pop(5)
                    for k in range(len(a)):
                        seq1.append(a[k])
                # inserting node ids, layer ids,time and value into inter-layer list table
                cr.execute(" INSERT INTO " + multiplex +"(node1, node2, layer1, layer2, time, id) VALUES(%s, %s, %s, %s, %s, %s)" ,
                (seq1[0], seq1[1], seq1[2], seq1[3], seq1[4], c))
                for i in range(max_length - 5):
                    value = "value" + str(i+1)
                    try:
                        cr.execute("UPDATE " + multiplex + " SET " + value + "= %s WHERE id = %s" , (seq1[i+5], c))
                    except:
                        cr.execute("UPDATE " + multiplex + " SET " + value + "= %s WHERE id = %s" , (None, c))
                c += 1
        
        # opening inter-layer file
        inter_layer_file = open('%s.txt'% inter_layer, "r")
        # store all edges from inter-layer list file
        for line2 in inter_layer_file:
            seq2 = line2.split()
            for j in range(4):
                seq2[j] = self.enc(seq2[j])
            if "[" in seq2[5]:
                newstr1 = seq2[5].replace("[", "")
                newstr2 = newstr1.replace("]", "")
                newstr3 = newstr2.replace("'", "")
                b = newstr3.split(",")
                seq2.pop(5)
                for k in range(len(b)):
                    seq2.append(b[k])
            # inserting node ids, layer ids,time and value into inter-layer list table
            cr.execute(" INSERT INTO " + multiplex +"(node1, node2, layer1, layer2, time, id) VALUES(%s, %s, %s, %s, %s, %s)" ,
            (seq2[0], seq2[1], seq2[2], seq2[3], seq2[4], c))
            for i in range(max_length - 5):
                value = "value" + str(i+1)
                try:
                    cr.execute("UPDATE " + multiplex + " SET " + value + "= %s WHERE id = %s" , (seq2[i+5], c))
                except:
                    cr.execute("UPDATE " + multiplex + " SET " + value + "= %s WHERE id = %s" , (None, c))
            c += 1
            
        # deleting the id column
        cr.execute("ALTER TABLE " + multiplex + " DROP COLUMN id ")
        
def parse_arguments():
    parser = argparse.ArgumentParser(description=
        """Create Multiplex Format and Store in the MySQL Database""")
    parser.add_argument("username", help="username")
    parser.add_argument("password", help="password")
    parser.add_argument("network", help="network name") 
    
    return parser.parse_args()  
                                
def main():
    args = parse_arguments()
    # draw is the object of class drawing
    m = Multiplex()
    
    db = m.connect_to_db(args.username,args.password)            # connecting to databse
    cursor = db.cursor()                 # creating cursor
    
    db_name = str(args.network) + "_db"          # giving name to database
    multiplex = str(args.network) + "_multiplex"       # giving name to multiplex 
    layer = str(args.network) + "_layer_list"     # giving name to layer list 
    node = str(args.network) + "_node_list"     # giving name to node list 
    intra_layer = str(args.network) + "_intra_layer_list"   # giving name to intra layer list 
    inter_layer = str(args.network) + "_inter_layer_list"   # giving name to inter layer list 
    
    m.create_db(cursor, db_name)
    layer_list = m.create_layer_list(cursor, layer)
    m.create_node_list(cursor, node)
    m.create_inter_layer_list(cursor, inter_layer)
    m.create_intra_layer_lists( cursor, intra_layer, layer_list)
    m.create_multiplex(cursor, multiplex, intra_layer, inter_layer, layer_list)
    
    # closing database connection
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()