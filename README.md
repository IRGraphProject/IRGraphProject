# IRGraphProject

## A collection of Python scripts useful to calculate graph measurements and visualize word-cooccurrence graphs.

### Data

Our corpora include simple and standard language, using both English Wikipedia and German news ressources.

### Scope

All works were conducted as an university research project for the course "Advanced Methods of Information Retrieval".

### Project and directory structure

* `news` and `wiki` directories contain scripts for
    * crawling nachrichtenleicht.de resp. downloading Wikipedia articles, and
    * specific tools for scraping, preprocessing and storing the data obtained, transforming them into text corpora for further work.
* Next, the ASV toolchain was used to calculate cooccurrences (coocs) on these corpora, and the results of these calculations were stored to a MySQL db in standardized form.
* The scripts included in `cooccurrences` were used to dump the coocs as csv and clean them.
* `data` holds the cooccurrence data we used (csv format).
* We used Python graph-tool to create coccurrence graphs, do graph calculations and graph visualisations. The scripts were stored into `graph_tool`.
* Intermediate and final results were saved to `data/results`.
* The `R` directory holds an R script for visualizing histogram data from these results.
* Finally, `doc` contains the report that was created to document the working process and its outcomes.
