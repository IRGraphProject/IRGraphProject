#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
import math
import argparse
from wordsgraph import WordsGraph
import graph_parser

## handle arguments from command line
parser = argparse.ArgumentParser(description='Create a cooccurrence graph and print out some measures')
parser.add_argument('-i', type=str, default="../data/test_data_aufsichtsrat",
    help="input file containing cooccurrences (default: ../data/test_data_aufsichtsrat)")
parser.add_argument('-o', type=str, default="testout.png",
    help="PNG output file (default: testout.png)")
parser.add_argument('-w', type=str, default="Aufsichtsrat",
    help="word to retrieve cooccurrences from (default: Aufsichtsrat)")
parser.add_argument('-d', type=int, default=1,
    help="iteration depth; maximum distance to word (default: 1)")
args = parser.parse_args()
# assign arguments to variables
infile = args.i
outfile = args.o
word = args.w
depth = args.d

# function: define layout and draw graph
def draw_wordsgraph(wordsgraph):
    # define layout
    layout = sfdp_layout(wordsgraph.graph, C=0.1, eweight=wordsgraph.eprop_value_float)
    # draw graph
    graph_tool.draw.graph_draw(wordsgraph.graph,layout, vertex_text=wordsgraph.vprop_word_string,
        output_size=(1000,1000), output=outfile,
        vertex_size=10, edge_pen_width=2, vertex_text_position=7*math.pi/4,
        vertex_text_color='#2E6A7F', edge_color = wordsgraph.eprop_value_float)

# erzeuge aus der Datei test_data_NL einen WordGraph
# (siehe wordsgraph.py für weitere Dokumentation)
g = graph_parser.file_to_graph(infile)
print("graph created")

# graph_tool stellt eine möglichkeit zur Berechnung des Durchmessers eines
# Graphen zur Verfügung. Die Methode braucht dazu das graph_tool Graph objekt,
# welches in unserem WordsGraph-Objekt unter dem Feld graph erreichbar ist.
#print("pseudo diameter: %s" % str(graph_tool.topology.pseudo_diameter(g.graph)))
#print("global clustering: %s" % str(graph_tool.clustering.global_clustering(g.graph)))


# Macht einen Ausschnitt um das Wort Aufsichtsrat mit allen direkten Nachbarn.
# Achtung die Funktion ist noch nicht fertig, es werden nicht die Kookkurrenzen
# der Nachbarn untereinander übernommen.
#sg = g.make_subgraph_around('Aufsichtsrat', 1)
# muss dementsprechend 3 sein.
g.filter_cooccurrence_threshold(1/12)

sg = g.make_subgraph_around(word, depth)
#sg.filter_cooccurrence_threshold(1/15)
# muss dementsprechend 3 sein.
print("pseudo diameter subgraph: %s" % str(graph_tool.topology.pseudo_diameter(sg.graph)))

draw_wordsgraph(sg)
