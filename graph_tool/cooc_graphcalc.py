#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
import argparse
import math
import numpy as np
import os
import re
from nltk.corpus import stopwords
from wordsgraph import WordsGraph
import graph_parser

# functions ##################################################################
def draw_wordsgraph(word, graph, depth, outfile):
    """Draws a subgraph of all nodes up to ```depth``` around a node with
    identifier ```word``` from ```graph``` and writes it to ```outfile```."""
    try:
        # creates a section around $word containing all neighbors within $depth
        sg = g.make_subgraph_around(word, depth)
        # define layout
        layout = sfdp_layout(sg.graph, C=0.1, eweight=sg.eprop_value_float)
        # draw graph
        graph_tool.draw.graph_draw(sg.graph,layout,
            vertex_text=sg.vprop_word_string,
            output_size=(1000,1000), output=outfile,
            vertex_size=10, edge_pen_width=2, vertex_text_position=7*math.pi/4,
            vertex_text_color='#000000', edge_color = sg.eprop_value_float)
    except:
        pass

def write_vertex_degree_hist(wordsgraph, out_file):
    """Calculates a histogram of vertex degrees, say how often each vertex 
    degree occurs.
    The results are written to out_file. The first line contains the vertex 
    degrees (bins), the second line the counts.
    """
    counts, bins = graph_tool.stats.vertex_hist(wordsgraph.graph, 'total',
        float_count= False)
    counts = np.append(counts, 0)
    with open(out_file, 'w') as f:
        f.write(','.join(map(str, bins)))
        f.write('\n')
        f.write(','.join(map(str, counts)))
        f.write('\n')

def write_min_distance_hist(wordsgraph, out_file):
    """calculates a histogram of the minimum distances from each vertex to each
    other and writes it to out_file. The first line contains the distances
    between vertices (bins); the second line how often these distances occur
    (counts).
    see https://graph-tool.skewed.de/static/doc/stats.html#graph_tool.stats.distance_histogram
    """
    counts, bins = graph_tool.stats.distance_histogram(wordsgraph.graph,
        float_count= False)
    counts = np.append(counts, 0)
    with open(out_file, 'w') as f:
        f.write(','.join(map(str, bins)))
        f.write('\n')
        f.write(','.join(map(str, counts)))
        f.write('\n')

def filter_main_component(graph):
    """
    Filters largest set of interconnected nodes. Drops all small components
    that are not connected to the main set.
    """
    print("filtering for main component...")
    vertices_before = graph.graph.num_vertices()
    edges_before = graph.graph.num_edges()
    main_component = graph_tool.topology.label_largest_component(graph.graph)
    graph.graph.set_vertex_filter(main_component)
    vertices_after = graph.graph.num_vertices()
    edges_after = graph.graph.num_edges()
    print("vertices before: " + str(vertices_before))
    print("vertices after: " + str(vertices_after))  
    print("difference: " + str(vertices_before - vertices_after))
    print("edges before: " + str(edges_before))
    print("edges after: " + str(edges_after))
    print("difference: " + str(edges_before - edges_after))

def write_topn_vertices(words_graph, out_file):
    """writes the n vertices with the most edges into the given file
    Note: if there are more vertices with the same degree as the nth one
    all of these are collected
    """
    tops = [(words_graph.vprop_word_string[v], v.in_degree() + v.out_degree())
        for v in words_graph.graph.vertices()]
    # define stopwords
    swords = stopwords.words('english') + stopwords.words('german') + ['dass']
    # remove ALL the stopwords
    tops = [t for t in tops if t[0].lower() not in swords]
    tops = sorted(tops, key = lambda entry: entry[1])
    while tops[0][1] < tops[len(tops)-args.n][1]:
        tops.pop(0)
    tops.reverse()
    with open(out_file, 'w') as f:
        for word, count in tops:
            f.write(word)
            f.write(',')
            f.write(str(count))
            f.write('\n')
    return [t[0] for t in tops]

def write_graphfiles(word,tdir):
    """Create cooccurrence graph for word and write to 3 different files
    """
    print(' - drawing subgraph ' + word)
    # pdf files
    t1 = os.path.basename(''.join(['graph_', word, '.pdf']))
    t1 = os.path.join(tdir,t1)
    draw_wordsgraph(word, g, args.d, t1)
    # svg files
    t2 = os.path.basename(''.join(['graph_', word, '.svg']))
    t2 = os.path.join(tdir,t2)
    draw_wordsgraph(word, g, args.d, t2)
    # png files
    t3 = os.path.basename(''.join(['graph_', word, '.png']))
    t3 = os.path.join(tdir,t3)
    draw_wordsgraph(word, g, args.d, t3)

##############################################################################


## handle command line arguments
parser = argparse.ArgumentParser(description='Create a cooccurrence graph and \
    print out some measurements')
parser.add_argument('infile', help="input file containing cooccurrences")
parser.add_argument('outdir', help="output file directory")
parser.add_argument('-d', type=int, default=1,
    help="iteration depth; maximum distance to word (default: 1)")
parser.add_argument('-t', type=float, default=1/12,
    help="Cooccurrence threshold for graphs (default: 1/12)")
parser.add_argument("-g", "--graph", action="store_true",
    help="draw only graph/s (omit calculations)")
parser.add_argument('-o', action="store_true", help="omit drawing of top words")
parser.add_argument('-n', type=int, default=10,
    help="maximum number of words to draw graphs of (default: 10)")
parser.add_argument('-w','--words', help="list of words to retrieve \
        cooccurrences from", nargs='+')

args = parser.parse_args()

# create directory
try:
    os.mkdir(args.outdir)
except:
    if os.listdir(args.outdir): # dir not empty
        print('directory '+args.outdir+'/ not empty!')
        exit()
print('saving files to '+args.outdir+'/')

# create WordGraph from file (see wordsgraph.py for further doc)
print('creating graph for corpus '+args.infile)
g = graph_parser.file_to_graph(args.infile)
print('graph created')

# FILTER MAIN COMPONENT
filter_main_component(g)

# do calculations only if not in 'graph-only' mode
if not args.graph:
    print('doing calculations')
    vertex_degree_file = args.outdir + '/v_degree_hist.csv'
    min_dist_file = args.outdir + '/min_dist_hist.csv'

    # histograms for full graph
    write_vertex_degree_hist(g, vertex_degree_file)
    write_min_distance_hist(g, min_dist_file)
    print('wrote histograms')

    print('graph density: ' + str(g.density()))
    print('cluster coefficient: ' + str(g.clustercoefficient()))

# define max. relevant cooccurrence value
print('cooc. threshold filter applied (='+str(args.t)+")")
g.filter_cooccurrence_threshold(args.t)

if not args.o:
    tdir = os.path.join(args.outdir,'topwords')
    os.mkdir(tdir)
    # save top words to file
    topwords = write_topn_vertices(g, tdir + '/list.csv')
    print('wrote top' + str(len(topwords)))
    # save subgraph for each top n word
    print('drawing '+str(len(topwords))+' cooccurrence graph/s with max. depth '
        +str(args.d))
    for word in topwords:
        write_graphfiles(word,tdir)

if args.words:
    # save subgraph for each word given
    tdir = args.outdir
    print('drawing '+str(len(args.words))+' cooccurrence graph/s with  max.'
        +'depth '+str(args.d))
    for word in args.words:
        write_graphfiles(word,tdir)

print('done')
