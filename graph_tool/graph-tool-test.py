#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
import math
import argparse
import os
from wordsgraph import WordsGraph
import graph_parser
import re
import numpy as np

# functions ##################################################################
def draw_wordsgraph(word, graph, depth, outfile):
    """Draws a subgraph of all nodes up to ```depth``` around a node with
    identifier ```word``` from ```graph``` and writes it to ```outfile```."""
    try:
        # Macht einen Ausschnitt um das Wort mit allen Nachbarn bis Abstand depth
        sg = g.make_subgraph_around(word, depth)
        # define layout
        layout = sfdp_layout(sg.graph, C=0.1, eweight=sg.eprop_value_float)
        # draw graph
        graph_tool.draw.graph_draw(sg.graph,layout, vertex_text=sg.vprop_word_string,
            output_size=(1000,1000), output=outfile,
            vertex_size=10, edge_pen_width=2, vertex_text_position=7*math.pi/4,
            vertex_text_color='#2E6A7F', edge_color = sg.eprop_value_float)
    except:
        pass

def calculate_true_diameter(g):
    """Calculates the true diameter of a graph."""
    d = graph_tool.topology.shortest_distance(g.graph)
    return max([max(d[v].a) for v in g.graph.vertices()])

def write_vertex_degree_hist(wordsgraph):
    counts, bins = graph_tool.stats.vertex_hist(wordsgraph.graph, 'total', float_count= False)
    counts = np.append(counts, 0)
    with open(vertex_degree_file, 'w') as f:
        f.write('; '.join(map(str, bins)))
        f.write('\n')
        f.write('; '.join(map(str, counts)))

def write_min_distance_hist(wordsgraph):
    counts, bins = graph_tool.stats.distance_histogram(wordsgraph.graph, float_count= False)
    counts = np.append(counts, 0)
    with open(min_dist_file, 'w') as f:
        f.write('; '.join(map(str, bins)))
        f.write('\n')
        f.write('; '.join(map(str, counts)))
##############################################################################

## handle arguments from command line
parser = argparse.ArgumentParser(description='Create a cooccurrence graph and print out some measures')
parser.add_argument('outdir', help="(not-yet-existent) output file directory")
parser.add_argument('words', help="list of words to retrieve cooccurrences\
        from", nargs='+')
parser.add_argument('-i', default="../data/test_data_aufsichtsrat",
    help="input file containing cooccurrences (default: ../data/test_data_aufsichtsrat)")
parser.add_argument('-d', type=int, default=1,
    help="iteration depth; maximum distance to word (default: 1)")
parser.add_argument('-t', type=float, default=1/12,
    help="Cooccurrence threshold (default: 1/12)")

args = parser.parse_args()

# make directory
try:
    os.mkdir(args.outdir)
except:
    print("directory "+args.outdir+"/ already exists!")
    exit()

# erzeuge aus der Datei test_data_NL einen WordGraph
# (siehe wordsgraph.py für weitere Dokumentation)
g = graph_parser.file_to_graph(args.i)
print("graph created")

vertex_degree_file = args.outdir + '/v_degree_hist.csv'
min_dist_file = args.outdir + '/min_dist_hist.csv'
diameter_file = args.outdir + '/diameter.txt'

# histograms for full graph
write_vertex_degree_hist(g)
write_min_distance_hist(g)
print('wrote histograms')

with open(diameter_file, 'w') as fp:
    fp.write(str(calculate_true_diameter(g)))

# define max. relevant cooccurrence
g.filter_cooccurrence_threshold(args.t)

# save subgraph for each word given
for word in args.words:
    print('Drawing subgraph ' + word)
    t = os.path.basename('_'.join(['graph', word, '.png']))
    t = os.path.join(args.outdir,t)
    draw_wordsgraph(word, g, args.d, t)
