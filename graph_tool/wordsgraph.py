from graph_tool.all import *

class WordsGraph:
    def __init__(self):
        self.graph = Graph(directed=False)
        self.wordvertexes = {}
        self.vprop_word_string = self.graph.new_vertex_property("string")
        self.eprop_value_float = self.graph.new_edge_property("float")


    def get_vertex_id(self, word):
        if word in self.wordvertexes:
            return self.wordvertexes[word]
        else:
            return None

    def get_or_create_vertex(self, word):
        v = self.get_vertex_id(word)
        if( v == None ):
            v = self.graph.add_vertex()
            self.vprop_word_string[v] = word
            self.wordvertexes[word] = v
        return v

    def create_edge(self, word_from, word_to, value):
        vertex_from = self.get_or_create_vertex(word_from)
        vertex_to = self.get_or_create_vertex(word_to)
        edge = self.graph.add_edge(vertex_from, vertex_to)
        self.eprop_value_float[edge] = value


    def make_subgraph_around(self, word, depth):
        def _add_neighbours(graph, vertex, depth):
            if(depth == 0):
                return
            v_neighbours = vertex.all_edges()
            for neighbour in v_neighbours:
                graph.create_edge(self.vprop_word_string[vertex], self.vprop_word_string[neighbour.target()], self.eprop_value_float[neighbour] )
                #graph.get_or_create_vertex(self.vprop_word_string[neighbour.target()])
                if(depth > 0):
                    _add_neighbours(graph, self.graph.vertex(neighbour.target()), depth-1)

        subgraph = WordsGraph()
        start_id = self.get_vertex_id(word)
        start_vertex = self.graph.vertex(start_id)
        subgraph.get_or_create_vertex(word)
        _add_neighbours(subgraph, start_vertex, depth)
    #v_neighbours = start_vertex.all_neighbours()
    #    for neighbour in v_neighbours:
    #        subgraph.get_or_create_vertex(self.vprop_word_string[neighbour])
        return subgraph
