#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
from wordsgraph import WordsGraph
import graph_parser

g = graph_parser.file_to_graph('test_data_NL')
print("graph created")
print("pseudo diameter: %s" % str(graph_tool.topology.pseudo_diameter(g.graph)))
print("global clustering: %s" % str(graph_tool.clustering.global_clustering(g.graph)))


sg = g.make_subgraph_around('Merkel', 1)
print("pseudo diameter subgraph: %s" % str(graph_tool.topology.pseudo_diameter(sg.graph)))



#layout = sfdp_layout(g, eweight=eprop_value_float, C=0.1)
#graph_tool.draw.graph_draw(g,layout, output_size=(10000,10000), output="testout.png", vertex_size=10 )

#center = wordvertexes.values()[0]
#for v in wordvertexes.values():
#    if v.in_degree()+v.out_degree() > center.in_degree()+center.out_degree():
#        center=v
#radial_layout = radial_tree_layout(g, center)
