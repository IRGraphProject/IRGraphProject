#!/bin/sh
mkdir out
mkdir out/stdouts
python ./graph_tool/cooc_graphcalc.py -i ./data/cooc_nl.csv ./out/cooc_nl > out/stdouts/cooc_nl
python ./graph_tool/cooc_graphcalc.py -i ./data/cooc_wiki_en.csv ./out/cooc_wiki_en > out/stdouts/cooc_wiki_en
python ./graph_tool/cooc_graphcalc.py -i ./data/cooc_wiki_sim.csv ./out/cooc_wiki_sim > out/stdouts/cooc_wiki_sim
