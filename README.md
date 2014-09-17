# Tools for Multiplex Network Format Translation and Visualisation

This repository contains open-source software tools for converting multiplex network data 
files into the LASAGNE Multiplex Framework foramt.


## Files

The following Python files can be found in the `src` directory:

* connector_flight
* connector_terrorist

* multiplex_db
* multiplex_file

* multiplex_db_draw
* multiplex_file_draw

* centrality_db
* centrality_file

* disrupt_db
* disrupt_file

The following publicly available original network data files are available in the `public_source_datasets` directory:

* `flights`: Flights routes around the world. Originally available at [openflight](http://openflight.org).
* `noordin_top`: the Noordin Top dataset used in Sean F. Everton's book "Disrupting Dark Networks", originally available  [on this website](https://sites.google.com/site/sfeverton18/research/appendix-1). The original Pajek (.paj) file has been split into the four text files that can be found in the `noordin_top` directory:
  * `Trust.txt` -- Trust Network
  * `Operational.txt` -- Operational Network
  * `Business_Financial.txt` -- Business and Financial Network
  * `Communication.txt` -- Communication Network


## General Usage Notes

Please note that to execute any Python scripts which includes a MySQL DB generation the user needs MySQL server on the computer and a MySQL account and a password. (See "Requirements" below for more information.)

1. `connector_flight` converts raw data of flight data set into meta format.
*Command line arguments for connector_flight : name of the network and flight file (ex: flight flight.txt).*

2. `connector_terrorist` converts raw data of the Noordin Top terrorist data set into meta format.
*Command line arguments for connector_flight : name of the network and terrorist files (ex: terrorist a.txt b.txt ...).*

3. `multiplex_db` is a script which creates multiplex format of data sets and stores them in the database
There are 5 or more tables : multiplex table, nodelist table, layerlist table, inter-layer list table
and intra-layer list tables(depends on the number of layers). 
*Command line arguments for multiplex_db : username, password, name of the network.*

4. `multiplex_file` is a script which creates multiplex format of data sets and stores them in a file.
*Command line arguments for multiplex_file : name of the network.*

5. `multiplex_db_draw` is a script which draws multiplex network by getting data sets from the database.
*Command line arguments for multiplex_db_draw : username, password and name of the network.*

6. `multiplex_file_draw` is a script which draws multiplex network by getting data sets from the files.
*Command line arguments for multiplex_file_draw : name of the network.*

7. `centrality_db` is a script calculates centralities of the nodes and draws degree distribution graphs
and calculates correlations between each layer and multiplex form of the data sets by taking data sets from database
*Command line arguments for centrality_db : username, password and name of the network.*

8. `centrality_file` is a script calculates centralities of the nodes and draws degree distribution graphs
and calculates correlations between each layer and multiplex form of the data sets by taking data sets from files.
*Command line arguments for centrality_file : name of the network.*

9. `disrupt_db` is a script that draws the multiplex graph by getting data sets from database after disrupting the central node.
*Command line arguments for disrupt_db : username, password, name of the network and node to disrupt.*

10. `disrupt_file` is a script that draws the multiplex graph by getting data sets from files after disrupting the central node.
*Command line arguments for disrupt_files : name of the network and node to disrupt.*


# Requirements

The following Python packages are required:
* `networkx`
* `matplotlib`
* `numpy`
* `scipy`

In addition, to use the MySQL database output format, the Python `MySQLdb` module is required, and can be found in the `mysql-python` package. The assumed MySQL port is 3307.

