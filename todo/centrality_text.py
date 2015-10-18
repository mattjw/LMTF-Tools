""" 
Centrality measures on multiplex network by taking datas from files
"""
# Demet Turan <dxt261@cs.bham.ac.uk>

import sys
from numpy import zeros, matrix
from numpy import linalg as LA
import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats

class Centrality():
    
    # constructor of the class
    def __init__(self):
        pass
    
    # insert layerids into the list from the layerlist table
    def list_of_layer(self, layerlist):
        layer_list =[]
        f = open('%s.txt'% layerlist, "r")
        for line in f:
            seq = line.split()
            layer_list.append(int(seq[0]))
        return layer_list
        
    # find number of nodes in nodelist table
    def list_of_node(self, nodelist):
        node_list = []
        f = open('%s.txt'% nodelist, "r")
        for line in f:
            seq = line.split()
            node_list.append(int(seq[0]))
        return node_list
    
    # put the nodes in a dictionary
    def dic_of_node(self, nodelist):
        node_list = {}  # dictionary keeps nodeid as an item and counter as a value
        f = open('%s.txt'% nodelist, "r")
        counter = 1
        for line in f:
            seq = line.split()
            node_list[int(seq[0])] = counter
            counter += 1
        return node_list
        
    # put the layers in a dictionary
    def dic_of_layer(self, layerlist):
        layer_list = {}  # dictionary keeps nodeid as an item and counter as a value
        f = open('%s.txt'% layerlist, "r")
        counter = 1
        for line in f:
            seq = line.split()
            layer_list[int(seq[0])] = counter
            counter += 1
        return layer_list
            
    # create adjacency matrix
    def create_matrix(self, multiplex, node, layer, dic_of_nodes, dic_of_layers):
        mat = matrix(zeros([node*layer, node*layer]))
        f = open('%s.txt'% multiplex, "r")
        for line in f:
            seq = line.split()
            """ 
            for instance node1=5, node2=10, layer1=1, layer2=3 ,
            then m= 5+ node*(1-1) -1 , here m=4 
            """
            m = int(dic_of_nodes[int(seq[0])]) + node * (int(dic_of_layers[int(seq[2])])-1) - 1
            # and n= 10+ node*(1-1) -1 , here n=9
            n = int(dic_of_nodes[int(seq[1])]) + node * (int(dic_of_layers[int(seq[3])])-1) - 1
            # if there is an edge between two nodes, then the adjacency matrix mat[m,n]=1
            mat[m,n] = 1.0
        return mat
        
    #degree centrality of each node in each layer
    def degree_cent(self, node, layer, list_of_nodes, M):
        
        list_cent_layer = []
    
        for x in range(layer):
            list_centrality = {}
            for i in range(node):
                ro = 0
                for j in range(node*layer):
                    # for i=0, ro = M[0,0]+...+M[0,node*layer-1]
                    ro += M[i+ x*node, j]
                list_centrality[list_of_nodes[i]] = ro
            list_cent_layer.append(list_centrality)
        return list_cent_layer

    # cumulative degree distribution of each layer
    def degree_dist(self, list_of_cent_all_layer, node):
    
        for p in range(len(list_of_cent_all_layer)):
            # new_layer is one of the element of list which has degree centrality of each node in each layer
            new_layer = list_of_cent_all_layer[p]
            
            # create a new figure for each plot
            fig = plt.figure(p+5)
            ax = fig.add_subplot (111)
            x = sorted(new_layer.values())
            cdf =stats.norm.cdf(x)
            #ax.hist(new_layer.values())
            # plot cdf function of degrees
            ax.plot(x, cdf)
            plt.title(str(p+1)+ ". layer cumulative degree distribution")
            plt.xlabel("degree")
            plt.ylabel("P(Degree <= degree)")
            

    # list of all neighbors of each node  
    def list_of_neighbours(self, node, layer, list_of_nodes, M):
        m = {}       # m is the dictionary keeping nodes and their neighbours
        for i in range(node):
            n =[]     # n is the list of neighbours for a node in all layers
            while i< (node*layer):
                l =[]  # l is the list of neighbours for a node in one layer
                for j in range(node*layer):
                    if int(M[i,j]) != 0 :
                        # r returns the j to the nodeid
                        r = j% node
                        # if there is an egde between i and j put j(=r) in a list as a neighbour of i
                        l.append(list_of_nodes[r])
                n.append(l)
                i += node
            m[list_of_nodes[i-node*layer]] = n
        return m
        
    # number of union of the sets of the neighbors for each node
    def union(self, list_of_nodes, neighbours, layer):
        m = {}    # m is the dictionary keeping nodes and union of the neighbours
        for i in list_of_nodes:
            un = set().union(*neighbours[i]) 
            m[i] = (float(len(un)) / (layer*(len(list_of_nodes)-1))) *100
        return m
        
    # draw union degree distribution
    def union_degree_dist(self, uni, node):
        x = sorted(uni.values())
        cdf =stats.norm.cdf(x)
        # create a new figure for the plot
        fig = plt.figure(1)
        ax = fig.add_subplot (111)
        # plot cdf function of degrees
        ax.plot(x, cdf)
        plt.title("union cumulative degree distribution")
        plt.xlabel("degree")
        plt.ylabel("P(Degree <= degree)")
        
    # number of intersection of the sets of the neighbors of node 1
    def intersection(self, list_of_nodes, neighbours):
        m = {}   # m is the dictionary keeping nodes and intersection of the neighbours
        for i in list_of_nodes:
            n = neighbours[i]
            intersect = set(n[0]).intersection(*n)
            m[i] = (float(len(intersect)) / (len(list_of_nodes)-1)) *100
        return m
        
    #diversity matrix
    def diversity_matrix(self, node, layer, M):
        D = matrix(zeros([node, node]))    # new matrix of size node*node
        
        for i in range(node):
            for j in range(node):
                s = 0.0
                for k in range(layer):
                    for l in range(layer):
                        # s is the degree of a node in each layer
                        s += M[(i+(node*k)),(j+(node*l))]
                # new matrix elements are total degree/ layer number
                D[i,j] = s/layer
             
        return D
        
    # degree centrality of each nodes  via diversity matrix  
    def div_strength_cent(self, node, list_of_nodes, D):
        list_centrality = {}
        
        for i in range(0,node):
            ro = 0
            for j in range(0,node):
                # for i=0, ro = D[0,0]+...+D[0,node-1]
                ro += D[i,j]
            # normalized strength centrality and expressed as a percentage
            list_centrality[list_of_nodes[i]] = (float(ro)/node)*100

        return list_centrality
        
    # degree distribution of each node over diversity matrix
    def diversity_strength_dist(self, list_cent, node):
        x = sorted(list_cent.values())
        cdf =stats.norm.cdf(x)
        # create a new figure for the plot
        fig = plt.figure(3)
        ax = fig.add_subplot (111)
        # plot the cdf function
        ax.plot (x,cdf)
        #ax.hist(list_cent.values())
        plt.title("diversity strength distribution")
        plt.xlabel("strength")
        plt.ylabel("P(Strength <= strength)")

    #correlation between each layer and multiplex
    def correlation(self, list_cent,list_of_cent_all_layer):
        # list for correlation and p values for each layer
        list_corr = []
        for p in range(len(list_of_cent_all_layer)):
            # new_layer is one of the element of list which has degree centrality of each node in each layer
            new_layer = list_of_cent_all_layer[p]
            sort_layer = sorted(new_layer.items())
            list_layer = [v for (k, v) in sort_layer]
            sort_multiplex = sorted(list_cent.items())
            list_multiplex = [v for (k, v) in sort_multiplex]
            corr = stats.spearmanr(list_layer, list_multiplex)
            list_corr.append(corr)
        print str("correlations\n") + str(list_corr)    
        return list_corr
    # draw correlation between each layer and multiplex
    def draw_correlation(self, list_cent, list_of_cent_all_layer):

        for p in range(len(list_of_cent_all_layer)):
            # new_layer is one of the element of list which has degree centrality of each node in each layer
            new_layer = list_of_cent_all_layer[p]
            sort_layer = sorted(new_layer.items())
            list_layer = [v for (k, v) in sort_layer]
            sort_multiplex = sorted(list_cent.items())
            list_multiplex = [v for (k, v) in sort_multiplex]
            # create a new figure for each plot
            fig = plt.figure(p+5+len(list_of_cent_all_layer))
            ax = fig.add_subplot (111)
            ax.plot(list_layer, list_multiplex, "ro")
            plt.title("Correlation between multiplex and layer "+ str(p+1))
            plt.xlabel("layer")
            plt.ylabel("multiplex")

    # list of eigenvector centrality of each node
    def eigenvector_cent(self, node, max_eigenvalue, D, list_of_nodes, list_cent):
        eigenvector_centrality = {}
        # matrix multiplication of diversity matrix and centrality of each nodes
        for i in range(0,node):
            mult = 0
            for j in range(0,node):
                mult += (D[i,j] * list_cent[list_of_nodes[j]])
                
            eig_cent = ((1/max_eigenvalue) * mult)
            # normalized eigenvector centrality and expressed as a percentage   
            eigenvector_centrality[list_of_nodes[i]] = (eig_cent/node)*100
        
        return eigenvector_centrality

    # draw the diversity graph
    def draw_diversityGraph(self, node, D):
        #diversity graph
        G = nx.Graph()
        # adding nodes from the diversity matrix
        for i in range(0, node):
            G.add_node(i)
        # adding edges from diversity matrix
        for p in range(0, node):
            for q in range(0, node):
                if float(D[p,q]) != 0:
                    G.add_edge(p, q, weight = 1-D[p,q])
        return G
        
    # store all shortest paths in a list
    """
    the design of the list:
    list_of_path = {x : ([(path,y),(path,z)] ....}
    """
    def shortest_path(self, G, node, list_of_nodes):
        list_of_path = {}   # dictionary to keep node and shortest path to other nodes

        for x in range(node):
            # create a new temporary list to store the destination node and the path
            list_of_path2 = []
            for y in range(node):
                if x != y:
                    # x=beginning node y = destination node where x!=y
                    # find shortest path between them
                    try:
                        path = nx.dijkstra_path(G,x,y)
                    except:
                        path = []
                    # create a tuple with path and the destination node
                    tup = path, y
                    # store the all tuples in a list
                    list_of_path2.append(tup) 
            # store list with node itself into the dictionary
            list_of_path[list_of_nodes[x]] = list_of_path2
        return list_of_path
        
    # find closeness centrality of each node
    def closeness_cent(self, short, node):
        list_closeness = {}
        
        # for every element in shortest path list(p= item of the dict)
        for p in short:
            length = 0
            # for every element in the first element of tuple (short[p] = list, q=tuple)
            for q in short[p]:
                # take the multiplicative inverse of the length of the shortest path(q[0]=path) 
                # since if length is longer than the node is not closed to others
                try:
                    length += 1/float(len(q[0]))
                except:
                    length += 0.0
            # divide the sum of the lengths by (node-1) and express as a percentage
            closeness = (length / (node-1))*100
            list_closeness[p] = closeness
    
        return list_closeness
        
    # find betweenness centrality
    def betweenness_cent(self, G, list_of_nodes):
    
        betweenness = {}

        for i in G.nodes():
            ratio = 0
            for x in G.nodes():
                for y in G.nodes():
                    list_of_shortest_paths = []        # list for shortest paths which has node i
                    list_0f_all_shortest_paths = []    # list of all shortest paths
                    # if x != y look at the all shortest paths between x and y
                    if x != y:
                        try:
                            shortest_paths = nx.all_shortest_paths(G, source = x, target = y, weight ='weight')
                        except:
                            shortest_paths = []
                        # store each path in a list between x and y
                        try:
                            for p in shortest_paths:
                                list_0f_all_shortest_paths.append(p)
                                # if i (given node) is in any path, store that path in different list
                                if i in p:
                                    list_of_shortest_paths.append(p)
                        except:
                            list_of_shortest_paths = []
                            list_0f_all_shortest_paths = []
                        # length of shortest paths where x lies on / length of all shortest paths
                        try:
                            ratio += float(len(list_of_shortest_paths)) / float(len(list_0f_all_shortest_paths))
                        except:
                            ratio += 0.0
            # normalized betweennes centrality, expressed as a percentage        
            betweenness[list_of_nodes[i]] = (ratio/(len(list_of_nodes)*len(list_of_nodes)))*100                 
        
        return betweenness
    
    
        
def main(arg):
    # define an object of class Matrix
    mt = Centrality() 
    
    # define file names
    multiplex = str(arg) + "_multiplex"       # giving name to multiplex table
    nodelist = str(arg) + "_node_list"       # giving name to node list table
    layerlist = str(arg) + "_layer_list"     # giving name to layer list table
    # list of layers
    list_of_layers = mt.list_of_layer( layerlist)
    # length of layer list
    layer = len(list_of_layers)
    # list of nodes
    list_of_nodes = mt.list_of_node(nodelist)
    # dictionary of nodes
    dic_of_nodes = mt.dic_of_node(nodelist)
    # dictionary of layers
    dic_of_layers = mt.dic_of_node(layerlist)
    # length of node list
    node = len(list_of_nodes)
    # create adjacency matrix
    M = mt.create_matrix(multiplex, node, layer, dic_of_nodes, dic_of_layers)
    # degree centrality of each node in each layer
    list_of_cent_all_layer = mt.degree_cent(node, layer, list_of_nodes, M)
    # plot the degree distribution in each layer
    mt.degree_dist(list_of_cent_all_layer,node)
    # neighbours of each node in all layers
    neighbours = mt.list_of_neighbours(node, layer, list_of_nodes, M)
    # union neighbours of each node
    uni = mt.union(list_of_nodes, neighbours, layer)
    print str("union degree centrality\n")+str(
    max(uni.iterkeys(), key=lambda k: uni[k])) + ":"  + str(
    uni[max(uni.iterkeys(), key=lambda k: uni[k])]) 
    # plot union degree distribution
    mt.union_degree_dist(uni, node)
    # intersection neighnours of each node
    inter = mt.intersection(list_of_nodes, neighbours)
    print str("intersection degree centrality\n")+str(
    max(inter.iterkeys(), key=lambda k: inter[k])) + ":"  + str(
    inter[max(inter.iterkeys(), key=lambda k: inter[k])])
    # diversity matrix D
    D = mt.diversity_matrix(node, layer, M)
    # list of degree centrality of each node via diversity matrix
    list_cent = mt.div_strength_cent(node, list_of_nodes, D)
    print str("diversity strength centrality\n")+str(
    max(list_cent.iterkeys(), key=lambda k: list_cent[k])) + ":"  + str(
    list_cent[max(list_cent.iterkeys(), key=lambda k: list_cent[k])])
    # correlation between each layer and multiplex
    mt.correlation(list_cent,list_of_cent_all_layer)
    # draw correlations
    mt.draw_correlation(list_cent, list_of_cent_all_layer)
    # plot the diversity degree distribution
    mt.diversity_strength_dist(list_cent, node)
    # eigenvalues of diversity matrix
    eigen = LA.eigvals(D)
    # maximum eigenvalue
    max_eigenvalue = max(eigen)
    # eigenvector centrality of each node
    eig = mt.eigenvector_cent(node, max_eigenvalue, D, list_of_nodes, list_cent)
    print str("eigenvector centrality\n")+str(
    max(eig.iterkeys(), key=lambda k: eig[k])) + ":" + str(eig[max(eig.iterkeys(), key=lambda k: eig[k])])
    # draw the diversity Graph
    G = mt.draw_diversityGraph(node, D)
    # all shortest paths of diversity graph
    short = mt.shortest_path(G, node, list_of_nodes) 
    # closeness centrality of each node in diversity graph
    cc = mt.closeness_cent(short, node)
    print str("closeness centrality\n")+str(
    max(cc.iterkeys(), key=lambda k: cc[k])) + ":" + str(cc[max(cc.iterkeys(), key=lambda k: cc[k])])                            
    #betweenness centrality of each node is diversity graph 
    bc = mt.betweenness_cent(G, list_of_nodes)
    print str("betweenness centrality\n")+str(
    max(bc.iterkeys(), key=lambda k: bc[k])) + ":" + str(bc[max(bc.iterkeys(), key=lambda k: bc[k])])

    
    plt.show()
    
    
if __name__ == '__main__':
    main(str(sys.argv[1]))