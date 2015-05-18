#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  puts the deu_news corpus into MongoDB

import datetime
import json
import pymongo
import re

con = pymongo.Connection('127.0.0.1', port=27017)
nachrichtenleicht = con.newsdb.nachrichtenleicht
denews2010 = con.newsdb.denews2010

corpusfile = open("data/deu_news_2010_10K-text/deu_news_2010_10K-sentences.txt","r")

for line in corpusfile:
	line = re.sub('^\d+\t','',line) 	#skip line numbering
	line = re.sub('\n','',line) 		#skip newlines
	denews2010.insert({ "text": line })
#	print line

con.disconnect()
