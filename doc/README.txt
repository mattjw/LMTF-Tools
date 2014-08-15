Drawing and creating multiplex format and analyse of multiplex network datas   23/08/2013
============================


FILES
-------------------
connector_flight (python file)
connector_terrorist (python file)

multiplex_db (python file)
multiplex_file (python file)

multiplex_db_draw (python file)
multiplex_file_draw (python file)

centrality_db (python file)
centrality_file (python file)

disrupt_db (python file)
disrupt_file (python file)


Terrorist data set:
Trust Network (text file)
Operational Network (text file)
Business and Financial Network (text file)
Communication Network (text file)


Flight data set:
flight (text file)


GENERAL USAGE NOTES
---------------------------

1- Connector_flight converts raw data of flight data set into meta format.

Command line arguments for connector_flight : name of the network and flight file (ex: flight flight.txt)


2- Connector_terrorist converts raw data of terrorist data set into meta format.

Command line arguments for connector_flight : name of the network and terrorist files (ex: terrorist a.txt b.txt ...)


3- To compile all python scripts which includes db user needs mysql server on the 
computer and a mysql account and a password


4- multiplex_db is a script which creates multiplex format of data sets and stores them in the database
There are 5 or more tables : multiplex table, nodelist table, layerlist table, inter-layer list table
and intra-layer list tables(depends on the number of layers)

Command line arguments for multiplex_db : username, password, name of the network


5- multiplex_file is a script which creates multiplex format of data sets and stores them in a file

Command line arguments for multiplex_file : name of the network


6- multiplex_db_draw is a script which draws multiplex network by getting data sets from the database

Command line arguments for multiplex_db_draw : username, password and name of the network


7- multiplex_file_draw is a script which draws multiplex network by getting data sets from the files

Command line arguments for multiplex_file_draw : name of the network


8- centrality_db is a script calculates centralities of the nodes and draws degree distribution graphs
and calculates correlations between each layer and multiplex form of the data sets by taking data sets from database

Command line arguments for centrality_db : username, password and name of the network


9- centrality_file is a script calculates centralities of the nodes and draws degree distribution graphs
and calculates correlations between each layer and multiplex form of the data sets by taking data sets from files

Command line arguments for centrality_file : name of the network


10- disrupt_db is a script that draws the multiplex graph by getting data sets from database after disrupting the central node

Command line arguments for disrupt_db : username, password, name of the network and node to disrupt


11- disrupt_file is a script that draws the multiplex graph by getting data sets from files after disrupting the central node

Command line arguments for disrupt_files : name of the network and node to disrupt





HOW TO INSTALL MYSQL SERVER
------------------------------------

1- Download mysql installer 5.5 or higher version

2- Install the program

3- After installation be sure that port number is 3307

4- Add root password

5- If you want, create another user


LÝBRARÝES TO ýNSTALL
--------------------------

1- networkx

2- matplotlib

3- numpy

4- scipy