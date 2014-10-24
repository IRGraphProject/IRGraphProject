#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_tool.all import *
from wordsgraph import WordsGraph

# liest eine .csv-Datei ein und erzeugt einen WordsGraph daraus. Jede Zeile muss 3 Werte haben, die ersten Beiden die Wörte zwischen denen eine Kookkurrenz besteht und als drittes den Wert der Kookkurrenz
def file_to_graph(filename):
    wordsgraph = WordsGraph()

    infile = open(filename)
    for line in infile:
        l = line.split(', ')
        wordsgraph.create_edge(l[0], l[1], l[2])
    return wordsgraph
