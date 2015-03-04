#!/bin/sh
#mkdir data/results
#python3 ./graph_tool/cooc_graphcalc.py -i ./data/cooc_nl.csv ./out/cooc_nl > out/stdouts/cooc_nl
date
python3 ./graph_tool/cooc_graphcalc.py ./data/cooc_wiki_en.csv ./data/results/cooc_wiki_en > run_wiki_en
date
echo "first one done!"
python3 ./graph_tool/cooc_graphcalc.py ./data/cooc_wiki_sim.csv ./data/results/cooc_wiki_sim > run_wiki_sim
date
