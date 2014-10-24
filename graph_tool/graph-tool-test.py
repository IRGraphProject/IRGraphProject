#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
from wordsgraph import WordsGraph
import graph_parser

# erzeuge aus der Datei test_data_NL einen WordGraph (siehe wordsgraph.py für weite dokumentation)
g = graph_parser.file_to_graph('test_data_NL')
print("graph created")

# graph_tool stellt eine möglichkeit zur Berechnung des Durchmessers eines Graphen zur Verfügung. Die Methode braucht dazu das graph_tool Graph objekt, welches in unserem WordsGraph-Objekt unter dem Feld graph erreichbar ist.
#print("pseudo diameter: %s" % str(graph_tool.topology.pseudo_diameter(g.graph)))
#print("global clustering: %s" % str(graph_tool.clustering.global_clustering(g.graph)))


# Macht einen Ausschnitt um das Wort Aufsichtsrat mit allen direkten Nachbarn. Achtung die Funktion ist noch nicht fertig, es werden nicht die Kookkurrenzen der Nachbarn untereinander übernommen.
sg = g.make_subgraph_around('Aufsichtsrat', 1)
# muss dementsprechend 3 sein.
print("pseudo diameter subgraph: %s" % str(graph_tool.topology.pseudo_diameter(sg.graph)))

layout = sfdp_layout(sg.graph, C=0.1, eweight=sg.eprop_value_float)
graph_tool.draw.graph_draw(sg.graph,layout, vertex_text=sg.vprop_word_string, output_size=(1000,1000), output="testout.png", vertex_size=10 )
