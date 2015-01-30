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

def write_vertex_degree_hist(wordsgraph, out_file):
    """calculates a histogram of vertex degrees, say how often each vertex degree occurs.
    The results are written to out_file. The first line contains the vertex degrees (bins),
    the second line the counts.
    see 
    """
    counts, bins = graph_tool.stats.vertex_hist(wordsgraph.graph, 'total', float_count= False)
    counts = np.append(counts, 0)
    with open(out_file, 'w') as f:
        f.write(';'.join(map(str, bins)))
        f.write('\n')
        f.write(';'.join(map(str, counts)))
        f.write('\n')

def write_min_distance_hist(wordsgraph, out_file):
    """calculates a histogram of the minimum distances from each vertex to each other
    and writes it to out_file. The first line contains the distances between vertexes
    (bins); the second line how often these distances occur (counts).
    see https://graph-tool.skewed.de/static/doc/stats.html#graph_tool.stats.vertex_hist
    """
    counts, bins = graph_tool.stats.distance_histogram(wordsgraph.graph, float_count= False)
    counts = np.append(counts, 0)
    with open(out_file, 'w') as f:
        f.write(';'.join(map(str, bins)))
        f.write('\n')
        f.write(';'.join(map(str, counts)))
        f.write('\n')

def filter_main_component(graph):
    vertices_before = g.graph.num_vertices()
    edges_before = g.graph.num_edges()
    main_component = graph_tool.topology.label_largest_component(g.graph)
    g.graph.set_vertex_filter(main_component)
    vertices_after = g.graph.num_vertices()
    edges_after = g.graph.num_edges()
    print("filtering for main component")
    print("vertices before: " + str(vertices_before))
    print("vertices after: " + str(vertices_after))  
    print("difference: " + str(vertices_before - vertices_after))
    print("edges before: " + str(edges_before))
    print("edges after: " + str(edges_after))
    print("difference: " + str(edges_before - edges_after))

def write_top10_vertices(words_graph, out_file):
    """writes the 10 vertices with the most edges into the given file
    if there are more vertices with the same degree as the 10th one
    all of these are collected
    TODO this function needs to be tested!!!
    """
    tops = [(words_graph.vprop_word_string[v], v.in_degree() + v.out_degree()) for v in words_graph.graph.vertices()]
    tops = sorted(tops, key = lambda entry: entry[1])
    while tops[0][1] < tops[len(tops)-10][1]:
        tops.pop(0)
    print(tops)
    tops.reverse()
    with open(out_file, 'w') as f:
        for word, count in tops:
            f.write(word)
            f.write(';')
            f.write(str(count))
            f.write('\n')    
          
##############################################################################

## handle arguments from command line
parser = argparse.ArgumentParser(description='Create a cooccurrence graph and \
    print out some measurements')
parser.add_argument('outdir', help="output file directory")
parser.add_argument('-i', default="../data/test_data_aufsichtsrat.csv",
    help="input file containing cooccurrences (default: \
        ../data/test_data_aufsichtsrat.csv)")
parser.add_argument('-d', type=int, default=1,
    help="iteration depth; maximum distance to word (default: 1)")
parser.add_argument('-t', type=float, default=1/12,
    help="Cooccurrence threshold (default: 1/12)")
parser.add_argument("-g", "--graph", help="draw only graph/s (omit calculations)",
                    action="store_true")
parser.add_argument('-w','--words', help="list of words to retrieve cooccurrences\
        from", nargs='+')

args = parser.parse_args()

if args.graph and not args.words:
    print('must specify word/s to draw cooccurrence graphs of (-w)')
    exit()

# make directory
try:
    os.mkdir(args.outdir)
except:
    if os.listdir(args.outdir): # dir not empty
        print('directory '+args.outdir+'/ not empty!')
        exit()
print('saving files to '+args.outdir+'/')

# erzeuge aus der Datei test_data_NL einen WordGraph
# (siehe wordsgraph.py für weitere Dokumentation)
print('creating graph for corpus '+args.i)
g = graph_parser.file_to_graph(args.i)
# define max. relevant cooccurrence value
print('cooc. threshold = '+str(args.t))
g.filter_cooccurrence_threshold(args.t)
# this irreversibly removes all filtered vertices, needed, because we do
# filter again
g.graph.purge_vertices()
g.graph.purge_edges()
print('graph created')

# HIER GRAPH UM ALLES AUSSER HAUPTKOMPONENTE BESCHNEIDEN
filter_main_component(g.graph)
# this irreversibly removes all filtered vertices, needed, when we want to filter
# again later. We are not interested in the filtered vertices anyways.
g.graph.purge_vertices()

# do calculations only if not in 'graph-only' mode
if not args.graph:
    print('doing calculations')
    vertex_degree_file = args.outdir + '/v_degree_hist.csv'
    min_dist_file = args.outdir + '/min_dist_hist.csv'
    diameter_file = args.outdir + '/diameter.txt'

    # histograms for full graph
    write_vertex_degree_hist(g, vertex_degree_file)
    write_min_distance_hist(g, min_dist_file)
    print('wrote histograms')

    write_top10_vertices(g, args.outdir + '/top10.txt')
    print('wrote top10')

    print('graph density: ' + str(g.density()))
    print('clustercoefficient: ' + str(g.clustercoefficient()))

    with open(diameter_file, 'w') as fp:
        fp.write(str(calculate_true_diameter(g)))

if args.words:
    # save subgraph for each word given
    print('drawing '+str(len(args.words))+' cooccurrence graph/s with \
        max. depth '+str(args.d))
    for word in args.words:
        print(' - drawing subgraph ' + word)
        t = os.path.basename('_'.join(['graph', word, '.png']))
        t = os.path.join(args.outdir,t)
        draw_wordsgraph(word, g, args.d, t)

print('done')
