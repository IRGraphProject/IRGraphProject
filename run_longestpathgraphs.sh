# nachrichtenleicht
date
./graph_tool/cooc_graphcalc.py data/cooc_nl.csv graphs/nl -g -o -d 5 -w Seymour Hoffman America Dschasira Israelis "O’Toole" stellt Bowie > graphs/run_nl
date
# denews
./graph_tool/cooc_graphcalc.py data/cooc_denews10k.csv graphs/den -g -o -d 4 -w dar Erwachsenen Hans-Rudolf Financial E-Mail Guido zehnte Metzelder Pauli Kaymer Microsoft davor Aigner Bommel Hillary > graphs/run_den
# wiki-sim
date;./graph_tool/cooc_graphcalc.py data/cooc_wiki_sim.csv graphs/wsi -g -o -d 5 -w dar Guevara Mardi Kamui allgemeine scientology stoker splash DiCaprio Tannadice Caro carriageway depecheKazimir supersonic pernicious > graphs/run_wsi;date
