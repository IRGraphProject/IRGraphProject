#!/usr/bin/python
# -*- coding: utf-8 -*-
from graph_tool.all import *
from wordsgraph import WordsGraph

def file_to_graph(filename):
    wordsgraph = WordsGraph()

    infile = open(filename)
    for line in infile:
        l = line.split(', ')
        wordsgraph.create_edge(l[0], l[1], l[2])
    return wordsgraph
