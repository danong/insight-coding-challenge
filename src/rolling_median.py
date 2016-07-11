import sys
from statistics import median
import datetime
import json

class Graph(object):
    """ Simple graph implementation using dicts """
    def __init__(self, in_graph_dict={}):
        """ Initialize graph. Empty by default """
        self.__graph_dict = in_graph_dict
        self.__latest_timestamp = datetime.datetime(1901, 1, 1, 0, 0, 0)
            
    def add_edge(self, edge, timestamp):
        """ Add edge between two vertices. An edge is a set/tuple/list of two vertices and a timestamp. This is skipped if the timestamp is 60 seconds before latest timestamp. If the new edge has the latest timestamp, we remove all edges whose timestamps are 60 seconds or more before the new latest timestamp """
        time_difference = (timestamp - self.__latest_timestamp).total_seconds()
        # only add edge if timestamp is within 60 seconds of latest timestamp
        if time_difference > -60:
            (vertex1, vertex2) = tuple(edge)
            if vertex1 in self.__graph_dict:
                # check if edge already exists
                if vertex2 in [x[0] for x in self.__graph_dict[vertex1]]:
                    self.__graph_dict[vertex1] = [x for x in self.__graph_dict[vertex1] if x[0] != vertex2]  # remove old edge
                self.__graph_dict[vertex1].append((vertex2, timestamp)) # add new edge
            else:   # vertex1 not in dict yet
                self.__graph_dict[vertex1] = [(vertex2, timestamp)]         # just add vertex1 with vertex2 as the only edge
                
            if vertex2 in self.__graph_dict:    # repeat for vertex2 to vertex 1 edge
                if vertex1 in [x[0] for x in self.__graph_dict[vertex2]]:
                    self.__graph_dict[vertex2] = [x for x in self.__graph_dict[vertex2] if x[0] != vertex1]
                self.__graph_dict[vertex2].append((vertex1, timestamp))
            else:
                self.__graph_dict[vertex2] = [(vertex1, timestamp)]
        # if timestamp is later than previously latest_timestamp, update latest timestamp and remove edges more than a minute old
        if time_difference >= 0:
            # update timestamp
            self.__latest_timestamp = timestamp
            # remove old edges
            keys_to_delete = []
            for key in self.__graph_dict.keys():
                new_value = []
                for edge in self.__graph_dict[key]:
                    if (timestamp-edge[1]).total_seconds() < 60:
                        new_value.append(edge)
                if len(new_value) > 0:
                    self.__graph_dict[key] = new_value
                else:
                    keys_to_delete.append(key)
            # clean up
            for key in keys_to_delete:
                self.__graph_dict.pop(key)
                        
    def vertex_degree(self, vertex):
        """ Returns the degree of a vertex """
        adj_vertices = self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree
    
    def median_degree(self):
        """ Returns the median degree of all vertices in the graph """
        degrees = []
        for vertex in self.__graph_dict:
            degrees.append(self.vertex_degree(vertex))
        return median(degrees)
    
    def __str__(self):
        """ Format output string for easy debugging """
        repr = "Vertices: \n"
        for k in self.__graph_dict.keys():
            repr += k + ", "
        repr += "\nEdges: \n"
        for k, v in self.__graph_dict.items():
            repr += "{0}: {1}\n".format(k, v)
        return repr
    
def parse_timestamp(raw_ts):
    """ Parses input timestamp into Python datetime format. Input format YYYY-MM-DDTHH:MM:SSZ """
    # preprocess string
    time_string = raw_ts.replace("T", " ")
    time_string = time_string.replace("Z", "")
    # convert to python datetime
    dt = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    return dt
    
def parse_line(json_line, g):
    """ Call Graph.add_edge() function to update graph with new edge """
    g.add_edge([json_line['actor'], json_line['target']], parse_timestamp(json_line['created_time']))
    
if __name__ == "__main__":
    # get input and output file paths
    try:
        inFile = sys.argv[1]
        outFile = sys.argv[2] 
    except IndexError:
        print("Cannot open input/output arguments.")
        quit()
    # open input/output files file
    try:
        f1 = open(outFile, 'w')
        g = Graph()
        # get lines from input file
        with open(inFile, 'r') as f:
            for line in f:
                # try parsing input lines as JSON
                try:
                    parsed = json.loads(line)
                    # make sure no empty fields
                    if (len(parsed['target']) != 0) and (len(parsed['created_time']) != 0) and (len(parsed['actor']) != 0):
                        # update graph
                        parse_line(parsed, g)
                        # write median degree to output file
                        f1.write("{:.2f}\n".format(g.median_degree()))
                except ValueError:
                    print("JSON decoder failed!")
        # clean up
        f1.close()
        f.close()
    except IOError:
        print("Could not read file:", inFile)