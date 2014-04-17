#!/usr/bin/python
# -*- coding: utf-8 -*-
from graph_tool.all import *
import sys, codecs
reload(sys)
sys.setdefaultencoding("UTF-8")


def get_word_vertex(word, wordvertexes, v_word):
    if word in wordvertexes:
        vertex = wordvertexes[word]
    else:
        vertex = g.add_vertex()
        v_word[vertex] = word
        wordvertexes[word] = vertex
    return vertex

g = Graph(directed=False)
v_word = g.new_vertex_property("string")
e_value = g.new_edge_property("float")
wordvertexes = {}
infile = codecs.open('test_data_NL', encoding='utf-8')
for line in infile:
    l = line.split(', ')
    fromvertex = get_word_vertex(l[0], wordvertexes, v_word)
    tovertex = get_word_vertex(l[1], wordvertexes, v_word)
    edge = g.add_edge(fromvertex, tovertex)
    e_value[edge] = l[2]
   

layout = sfdp_layout(g, eweight=e_value, C=0.1)
graph_tool.draw.graph_draw(g,layout, output_size=(10000,10000), output="testout.png", vertex_size=10 )

center = wordvertexes.values()[0]
for v in wordvertexes.values():
    if v.in_degree()+v.out_degree() > center.in_degree()+center.out_degree():
        center=v
radial_layout = radial_tree_layout(g, center)
