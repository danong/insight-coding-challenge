##Challenge Summary

In this coding challenge, I generate a graph of Venmo transactions and calculate the running median degree for each vertex (i.e. user) in the graph.

##Implementation Details

My solution uses Python 3.5.2 and the sys, statistics, datetime, and json packages. I use the adjacency list graph model and keep track of edges using the Python dict data type. I also wrote a custom graph data type to support edges that have a timestamp to simplify keeping track of previous timestamps. 

##Execution

Execute the Python script by running the provided run.sh script located in the root folder. The 

##Speed/Scalability

This program can process the 1,792 given examples in 0.964s while running on my laptop (i5-4200U 2x1.6 GHz processor with 8GB RAM running Kubuntu 16.04). That's about 1850 transactions processed per second. If we were to expect more transactions per second, I would reimplement my algorithm using C++ for great speed/efficiency and use more powerful hardware.
