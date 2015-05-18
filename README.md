# IRGraphProject

## A collection of Python scripts useful to calculate graph measurements and visualize word-cooccurrence graphs.

### Data

Our corpora include simple and standard language, using both English Wikipedia and German news ressources.

### Scope

All works were conducted as an university research project for the course "Advanced Methods of Information Retrieval".

### Project and directory structure

* `news` and `wiki` directories contain several scripts for crawling nachrichtenleicht.de resp. downloading Wikipedia articles. There are also tools for scraping, preprocessing and storing the obtained data as text corpora for further work.
* Cooccurrences were calculated from these corpora by the ASV toolchain. These were stored to a MySQL db.
* Scripts in `cooccurrences` were used to dump them to csv files and clean these.
* `data` holds the cooccurrence data we used.
* Scripts for coccurrence graph creation, graph calculations and visualisations were stored in `graph_tool`.
* The results were saved to `data/results`.
* `R` -- scripts for visualizing histogram data from the previous steps, written in R.
* `doc` contains the report that was created to document the working process and outcomes.
