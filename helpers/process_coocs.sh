#!/bin/sh
# not really a proper shell script; copy + paste commands to your shell
# and edit as needed
grep eng_wiki.csv -ve "\s" > eng_wiki_clean.csv
fgrep eng_wiki_clean.csv -ve "'" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "&" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "'" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve ")" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "(" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "“" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "”" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "–" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve ":" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve ";" > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve "?" > eng_wiki_clean.csv 
sed -n 1~2p eng_wiki_clean.csv > eng_wiki_clean.csv 
fgrep eng_wiki_clean.csv -ve ",," > eng_wiki_clean.csv 
grep eng_wiki_clean.csv -ve ",.," > eng_wiki_clean.csv 
grep eng_wiki_clean.csv -ve "^.," > eng_wiki_clean.csv 
