import sys
from statistics import median
import datetime
import uuid
import json

DURATION = datetime.timedelta(seconds=60)

class Graph(object):
    """ Simple graph implementation using dicts """
    def __init__(self, in_graph_dict={}):
        """ Initialize graph. Empty by default """
        self.__graph_dict = in_graph_dict
        self.__latest_timestamp = datetime.datetime(1901, 1, 1, 0, 0, 0)
        
    def vertices(self):
        """ Return list of vertices """
        return list(self.__graph_dict.keys())
    
    def edges(self):
        """Return list of edges """
        return self.__generate_edges()
    
    def add_vertex(self, vertex):
        """ Add new vertex with no edges to graph """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
            
    def remove_edge(self, edge):
        """ Delete an edge from the graph """
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            pass
    def remove_vertex(self, vertex):
        """ Delete a vertex from the graph """
        pass
            
    def add_edge(self, edge, timestamp):
        """ Add edge between two vertices. An edge is a set/tuple/list of two vertices and a timestamp. This is skipped if the timestamp is 60 seconds before latest timestamp. If the new edge has the latest timestamp, we remove all edges whose timestamps are 60 seconds or more before the new latest timestamp """
        print(self.__latest_timestamp - timestamp)
        if timestamp > self.__latest_timestamp or (self.__latest_timestamp - timestamp > DURATION):
            (vertex1, vertex2) = tuple(edge)
            if vertex1 in self.__graph_dict:
                self.__graph_dict[vertex1].append((vertex2, timestamp))
            else:
                self.__graph_dict[vertex1] = [(vertex2, timestamp)]
            if vertex2 in self.__graph_dict:
                self.__graph_dict[vertex2].append((vertex1, timestamp))
            else:
                self.__graph_dict[vertex2] = [(vertex1, timestamp)]
                
            if 
            
    def __generate_edges(self):
        """ Generate all edges in graph """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges
    
    def vertex_degree(self, vertex):
        """ Returns the degree of a vertex """
        adj_vertices = self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        # remove disconnected nodes
        if degree == 0:
            self.remove_vertex(vertex)
        return degree
    
    def median_degree(self):
        """ Returns the median degree of all vertices in the graph """
        degrees = []
        for vertex in self.__graph_dict:
            degrees.append(self.vertex_degree(vertex))
        return median(degrees)
    
    def __str__(self):
        res = "Vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nEdges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res
    
def parse_timestamp(raw_ts):
    """ Parses input timestamp into Python datetime format. Input format YYYY-MM-DDTHH:MM:SSZ """
    # preprocess string
    time_string = raw_ts.replace("T", " ")
    time_string = time_string.replace("Z", "")
    # convert to python datetime
    dt = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    return dt
    
def parse_line(json_line, g):
    g.add_edge([json_line['actor'], json_line['target']], parse_timestamp(json_line['created_time']))
    
if __name__ == "__main__":
    dt1 = parse_timestamp('2016-04-07T03:33:19Z')
    dt2 = parse_timestamp('2016-04-07T03:34:19Z')
    if (dt2-dt1) > DURATION:
        print("should see this")
    # get input and output files
    try:
        inFile = sys.argv[1]
        outFile = sys.argv[2] 
    except IndexError:
        print("Cannot open input/output arguments.")
        quit()
    # open input file
    try:
        data = []
        g = Graph()
        with open(inFile, 'r') as f:
            for line in f:
                parse_line(json.loads(line), g)
                data.append(json.loads(line))
                print("Median degree: {:.2f}".format(g.median_degree()))
    except IOError:
        print("Could not read file:", inFile)
