#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
import math
import argparse
import os
from wordsgraph import WordsGraph
import graph_parser

## handle arguments from command line
parser = argparse.ArgumentParser(description='Create a cooccurrence graph and print out some measures')
parser.add_argument('words', help="list of words to retrieve cooccurrences\
        from", nargs='+')
parser.add_argument('-i', default="../data/test_data_aufsichtsrat",
    help="input file containing cooccurrences (default: ../data/test_data_aufsichtsrat)")
parser.add_argument('-p', default="graph", help="Output file prefix\
        (default: graph)")
parser.add_argument('-d', type=int, default=1,
    help="iteration depth; maximum distance to word (default: 1)")
parser.add_argument('-t', type=float, default=1/12,
    help="Cooccurrence threshold (default: 1/12)")

args = parser.parse_args()

def draw_wordsgraph(word, graph, depth, outfile):
    """Draws a subgraph of all nodes up to ```depth``` around a node with
    identifier ```word``` from ```graph``` and writes it to ```outfile```."""
    try: 
        sg = g.make_subgraph_around(word, depth)
        layout = sfdp_layout(sg.graph, C=0.1, eweight=sg.eprop_value_float)
        graph_tool.draw.graph_draw(sg.graph,layout, vertex_text=sg.vprop_word_string,
            output_size=(1000,1000), output=outfile,
            vertex_size=10, edge_pen_width=2, vertex_text_position=7*math.pi/4,
            vertex_text_color='#2E6A7F', edge_color = sg.eprop_value_float)
    except:
        pass

# erzeuge aus der Datei test_data_NL einen WordGraph
# (siehe wordsgraph.py für weitere Dokumentation)
g = graph_parser.file_to_graph(args.i)
print("graph created")

g.filter_cooccurrence_threshold(args.t)

for word in args.words:
    print('Drawing subgraph ' + word)
    t = os.path.basename('_'.join([args.p, word, '.png']))
    draw_wordsgraph(word, g, args.d, t)
