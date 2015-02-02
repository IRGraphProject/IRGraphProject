#!/bin/sh
mkdir data/results
#python3 ./graph_tool/cooc_graphcalc.py -i ./data/cooc_nl.csv ./out/cooc_nl > out/stdouts/cooc_nl
python3 ./graph_tool/cooc_graphcalc.py -i ./data/cooc_wiki_en.csv ./data/cooc_wiki_en > run_wiki_en
python3 ./graph_tool/cooc_graphcalc.py -i ./data/cooc_wiki_sim.csv ./data/cooc_wiki_sim > run_wiki_sim
