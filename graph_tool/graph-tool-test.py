#!/usr/bin/python
# -*- coding: utf-8 -*-
from graph_tool.all import *
import sys, codecs
reload(sys)
sys.setdefaultencoding("UTF-8")


class WordsGraph:
    def __init__(self):
        self.graph = Graph(directed=False)
        self.wordvertexes = {}
        self.vprop_word_string = self.graph.new_vertex_property("string")
        self.eprop_value_float = self.graph.new_edge_property("float")
        
        
    def get_vertex(self, word):
        if word in self.wordvertexes:
            return self.wordvertexes[word]
        else:
            return None

    def get_or_create_vertex(self, word):
        v = self.get_vertex(word)
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

            

def file_to_graph(filename):
    wordsgraph = WordsGraph()
    
    infile = codecs.open(filename, encoding='utf-8')
    for line in infile:
        l = line.split(', ')
        wordsgraph.create_edge(l[0], l[1], l[2])
    return wordsgraph

g = file_to_graph('test_data_NL')
print("graph created")
print("pseudo diameter: %s" % str(graph_tool.topology.pseudo_diameter(g.graph)))
print("global clustering: %s" % str(graph_tool.clustering.global_clustering(g.graph)))

#layout = sfdp_layout(g, eweight=eprop_value_float, C=0.1)
#graph_tool.draw.graph_draw(g,layout, output_size=(10000,10000), output="testout.png", vertex_size=10 )

#center = wordvertexes.values()[0]
#for v in wordvertexes.values():
#    if v.in_degree()+v.out_degree() > center.in_degree()+center.out_degree():
#        center=v
#radial_layout = radial_tree_layout(g, center)
