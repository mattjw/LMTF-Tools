# Tools for Multiplex Network Format Translation and Visualisation

This repository contains open-source software tools for converting multiplex network data 
files into the LASAGNE Multiplex Framework foramt.


## Files

The following Python files can be found in the `src` directory:

* connector_db_inter
* connector_db_inter_list
* connector_db_intra
* connector_db_intra_list
* connector_db_node_layer
* connector_flight
* connector_terrorist
* connector_brain
* connector_pardus
* generate\_multiplex\_text
* generate\_multiplex\_db
* generate\_multiplex\_brain_text
* generate\_multiplex\_brain_db
* draw\_multiplex_db
* draw\_multiplex_file




The following publicly available original network data files are available in the `public_source_datasets` directory:

* `flights`: Flights routes around the world. Originally available at [openflights](http://openflight.org).
* `noordin_top`: the Noordin Top dataset used in Sean F. Everton's book "Disrupting Dark Networks", originally available  [on this website](https://sites.google.com/site/sfeverton18/research/appendix-1). The original Pajek (.paj) file has been split into the four text files that can be found in the `noordin_top` directory:
  * `Trust.txt` -- Trust Network
  * `Operational.txt` -- Operational Network
  * `Business_Financial.txt` -- Business and Financial Network
  * `Communication.txt` -- Communication Network

## Connectors

Connectors are provided for 3 data formats. In all formats, inputs are raw text values(generally .txt files), separated by commas. The formats are:

### 1. Flight Dataset Format

This dataset is comprised of information about flights around the world. The original dataset can be downloaded [here](http://openflights.org/data.html).


Each of the files contains the following fields, separated by commas:

* Airline: 2-letter (IATA) or 3-letter (ICAO) code of the airline.
* Airline ID: Unique OpenFlights identifier for airline.
* Source Airport: 3-letter (IATA) or 4-letter (ICAO) code of the source airport.
* Airport ID: Unique OpenFlights identifier for source airport.
* Destination Airport: 3-letter (IATA) or 4-letter (ICAO) code of the destination airport.
* Destination Airport ID: Unique OpenFlights identifier for destination airport.
* Codeshare: "Y" if this flight is a codeshare (that is, not operated by Airline, but another carrier), empty otherwise.
* Stops: Number of stops on this flight (0 for direct).
* Equipment: 3-letter codes for plane type(s) generally used on this flight, separated by spaces.

### 2. Noordin Top's Terrorist Network Dataset Format

This dataset is comprised of links of different types in a terrorist network. The original dataset can be obtained [here](https://sites.google.com/site/sfeverton18/research/appendix-1).

The format of the data is the Pajek format, on which information can be obtained [here](http://pajek.imfm.si/doku.php).

### 3. Pardus Dataset Format

This dataset is comprised of links of different types between players of the online game Pardus, and is not publicly available. However, we are making the connector available, so identically formatted data can be converted nevertheless.
The Pardus connector takes as arguments multiple files, each representing a relational aspect(e.g., for the original Pardus data, friendship and foeship, messaging and trading).

Each of the files contains the following fields, separated by commas:

* Actor 1 
* Actor 2

### 4. Brain Dataset Format

This dataset is comprised of links of two types(functional and anatomical) in the brains of 45 subjects. It is not publicly available.
The dataset is composed of 46 files:
* one file with the anatomical connectivity (DTI) extracted from a group of subjects
* 45 files with functional connectivity from 45 different subjects

Each of the files contains the following fields, separated by commas:

* Node 1
* Node 2
* Connection strength



## General Usage Notes

Please note that, generally, being able to run a script depends on having run the previous ones in the logical order of the processing of the data.
The steps are:
    
    * If raw data is in SQL format, run specific database connectors to convert files to text format. If raw data is in text format, skip this step.
    * Run specific Original Data Connectors to convert raw data to meta format - input raw data can be either text or SQL
    * Run specific Multiplex Generation Tools to convert meta format data to LMTF multiplex format
    * Run Visualisation tools

Also note that to execute any Python scripts which includes a MySQL DB generation the user needs MySQL server on the computer and a MySQL account and a password. (See "Requirements" below for more information.)



### Database Connectors - Convert SQL raw data to text raw data (optional)

* `connector_db_inter` - converts inter-layer edge data in a SQL file to a text file
* `connector_db_inter_list` - same as above, but outputs a list of edges instead of having them separated by endline characters
* `connector_db_intra` - converts intra-layer edge data in a SQL file to a text file
* `connector_db_intra_list` - outputs a list of edges instead of having them separated by endline characters
* `connector_db_node_layer`- converts node and layer list data in a SQL file to a text file


Command line arguments for each of these scripts: mySQL username, mySQL password, database file name, table name



### Original Data Connectors - Convert raw data to meta format

There are two input possibilities, text format and SQL format. 

* `connector_flight` converts raw data of the Flight data set into meta format.
Command line arguments for connector_flight : name of the network and flight file (ex: python connector_flight.py flight flight.txt)

* `connector_terrorist` converts raw data of the Noordin Top terrorist data set into meta format.
Command line arguments for connector_terrorist : name of the network and terrorist files (ex: python connector_terrorist.py terrorist a.txt b.txt ...)

* `connector_pardus` converts raw data of the Pardus data set into meta format.
Command line arguments for connector_pardus : name of the network and pardus files (ex: python connector_pardus.py pardus a.txt b.txt ...)

* `connector_brain` converts raw data of the Brain data set into meta format.
Command line arguments for connector_pardus : name of the network and pardus files (ex: python connector_brain.py brain a.txt b.txt ...)

The output of running either of these scripts is the following:
1. `(network_name)_layer_list.txt`: contains a list of layers, separated by newline characters
2. `(network_name)_node_list.txt` : contains a list of nodes, separated by newline characters
3. `(network_name)_intra_layer_list.txt`: contains a list of edges between identical layers, separated by newline characters
4. `(network_name)_inter_layer_list_(id).txt`: contains a list of edges between different layers, separated by newline characters. Depending on the number of layers, multiple layer lists may be created.

The files above are created in the same directory as the script.

### Multiplex Generation Tools - Convert meta format data to LMTF multiplex format

There are two output possibilities:

1. Text output:

    * generate\_multiplex\_text is a script which creates multiplex format for input datasets and stores them in a text file.
    Command line arguments for generate\_multiplex\_text: name of the network

    * generate\_multiplex\_brain_text is a script which creates multiplex format for the brain input dataset and outputs to a text file.
    Command line arguments for generate\_multiplex\_brain\_text: name of the network

    The output goes to the file `(network_name)_multiplex.txt, in the same directory as the script.

2. SQL output:

    * generate\_multiplex\_db is a script which creates multiplex format for input datasets and stores them in a SQL database.
    Command line arguments for generate\_multiplex\_db : MySQL username, MySQL password, name of the network

    * generate\_multiplex\_brain\_db is a script which creates multiplex format for the brain input dataset and outputs to a SQL database.
    Command line arguments for generate\_multiplex\_brain\_db: MySQL username, MySQL password, name of the network

    The output goes to `(network_name)_db.db`.

Running the specific Original Data Connectors previously will create the appropriate files in the directory in order for the drawing tools to be able to run.


### Drawing Tools - Generate a simple visualisation of the network(Using raw and LMTF data)

* `draw_multiplex_text` is a script which draws a multiplex network by getting data from files.
Command line arguments for draw_multiplex_text : name of the network

* `draw_multiplex_db` is a script which draws a multiplex network by getting data from a database.
Command line arguments for draw_multiplex_text : MySQL username, MySQL password, name of the network.

* `draw_multiplex_top25` is a script which draws a multiplex network by getting data from files, drawing only the top 25 most connected nodes.
Command line arguments for draw_multiplex_text : name of the network

These three scripts require three files to be placed in the same directory as the script:
1. `(network_name)_multiplex.txt`: contains a list of edges in the format (node1 node2 layer1 layer2), each edge separated by newline characters
2. `(network_name)_node_list.txt`: contains a list of nodes, separated by newline characters
3. `(network_name)_layer_list.txt`: contains a list of layers, separated by newline characters

Running the specific Original Data Connectors and Multiplex Generation Tools previously will create the appropriate files in the directory in order for the drawing tools to be able to run.


# Requirements

The following Python packages are required:
* `argparse` (for Python 2.6 and earlier)
* `networkx`
* `matplotlib`
* `numpy`
* `scipy`

In addition, to use the MySQL database output format, the Python `MySQLdb` module is required, and can be found in the `mysql-python` package. The assumed MySQL port is 3307.

