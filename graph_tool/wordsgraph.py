from graph_tool.all import *

# graph_tool stellt graphen etwa wie folgt dar:
# * In einem Graph-Objekt (hier graph) liegen knoten(vertex) und kanten(edge), beide ausschließlich durch integerzahlen dargestellt
# * Eigenschaften von Knoten und Kanten liegen in vertex_properties bzw. edge_properties
# * diese sind Dictionarys: int(knoten/kanten-id)->string/float(wort/wert)
# In dieser Klasse sind die Teile zusammengefügt. Von aussen geht der Zugriff entweder über graph direkt, oder über die anderen Eigenschaften:
# * wordvertexes ist ein dict, dass für jedes Wort die zugehörige Knotenid speichert
# * vprop_word_string ist ein dict, dass jedem Knoten (daher das v wie vertex) ein Wort zuordnet
# * eprop_word_float ist ein dict, dass jeder Kante (daher das e wie edge) einen Wert zuordnet, für uns also der Kookkurrenzwert.
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

    # gibt den zugehörigen Knoten zu dem Wort word zurück (seine ID). Falls noch kein socher Knoten existiert wird ein neuer erzeugt.
    def get_or_create_vertex(self, word):
        v = self.get_vertex_id(word)
        if( v == None ):
            v = self.graph.add_vertex()
            self.vprop_word_string[v] = word
            self.wordvertexes[word] = v
        return v

    # Erzeugt eine Kante zwischen zwei Wörtern. word_from und word_to sind einfach die string-Wörter, die zugehörigen Knoten werden selbst rausgesucht.
    def create_edge(self, word_from, word_to, value):
        vertex_from = self.get_or_create_vertex(word_from)
        vertex_to = self.get_or_create_vertex(word_to)
        if(self.graph.edge(vertex_from, vertex_to) or self.graph.edge(vertex_to, vertex_from)):
            # do not create the edge again if it exists
            return
        edge = self.graph.add_edge(vertex_from, vertex_to)
        self.eprop_value_float[edge] = value

    # Erzeugt einen Teilgraphen um das Wort word, mit allen Knoten mit max Abstand depth. Es werden gerade noch nicht alle Edges hinzugefügt, hier ist noch etwas Arbeit zu tun, die Edges zwischen Nachbarn werden noch nicht übernommen.
    def make_subgraph_around(self, word, depth):
        def _add_neighbours(ngraph, vertex, depth):
            # ngraph ist der neue graph, die nachbarn von vertex im ursprungsgraph sollen übertragen werden.
            if(depth == 0):
                return
            v_neighbours = vertex.all_edges()
            for neighbour in v_neighbours:
                ngraph.create_edge(self.vprop_word_string[vertex], self.vprop_word_string[neighbour.target()], self.eprop_value_float[neighbour] )
                #graph.get_or_create_vertex(self.vprop_word_string[neighbour.target()])
                if(depth > 0):
                    _add_neighbours(ngraph, self.graph.vertex(neighbour.target()), depth-1)

        subgraph = WordsGraph()
        start_id = self.get_vertex_id(word)
        start_vertex = self.graph.vertex(start_id)
        subgraph.get_or_create_vertex(word)
        _add_neighbours(subgraph, start_vertex, depth)
        words = list(subgraph.wordvertexes.keys())
        for word in words:
            for target_word in words:
                edge = self.graph.edge(self.wordvertexes[word], self.wordvertexes[target_word])
                if edge:
                    subgraph.create_edge(word, target_word, self.eprop_value_float[edge])

    #v_neighbours = start_vertex.all_neighbours()
    #    for neighbour in v_neighbours:
    #        subgraph.get_or_create_vertex(self.vprop_word_string[neighbour])
        return subgraph
