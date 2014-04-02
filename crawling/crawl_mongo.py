#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Crawls nachrichtenleicht.de, extracts data and transfers data to MongoDB

import datetime
import HTMLParser
import json
import pymongo
import random
import re
import requests
import time
from StringIO import StringIO
from lxml import etree
from tidylib import tidy_document

# conntect to database
con = pymongo.Connection('127.0.0.1', port=27017)
nachrichtenleicht = con.newsdb.nachrichtenleicht
visited = con.newsdb.visited
# clear collection (if exists)
nachrichtenleicht.drop()

# keep track of visited/unvisited URLs
visitedURLs = set([])
newURLs = set([])

# resume from database
for row in visited.find({"visited": 0}):
	visitedURLs.add(row['url'])

for row in visited.find({"visited": 1}):
	newURLs.add(row['url'])

# do the crawling
def crawl(x):
	# mark page as visited
	visitedURLs.add(x)
	print("visited: "+x)

	# try update; if not working because URL not present: insert
	if ( not visited.update({'url': x}, {"$set": {'visited': 1}}, w=1)['updatedExisting'] ) :
		visited.insert({ "url": x, "visited" : 1 })

	# get HTML
	response = requests.get(x)
	document, errors = tidy_document(response.text, options={'indent': 0, 'char-encoding':'utf8', 'input-encoding':'utf8','output-encoding': 'utf8'})

	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(document.encode("utf-8")), parser)
	root = tree.getroot()

	# get content, if available
	if (root.find("body/div/div/div/div/div[@class='entry-content']/div[@class='detail_content']") is not None):
		# headline
		headline = root.findtext("body/div/div/div/div/div[@class='entry-content']/h2[@class='hl_title']")
		print("\tfound headline: "+headline)

		# teaser
		teaser = root.findtext("body/div/div/div/div/div[@class='entry-content']/div[@class='detail_teaser']/p")
		if (teaser is None): # some people use weird formatting in teaser; fixing this
			teaser = root.findtext("body/div/div/div/div/div[@class='entry-content']/div[@class='detail_teaser']/h2/strong")

		content = ''

		# find additional text (outside <p> tag)
		div = root.find("body/div/div/div/div/div[@class='entry-content']/div[@class='detail_content']")
		this = div.iterfind("dl")
		try:
			addtext = etree.tostring(this.next())
			addtext = re.sub('\n',' ',addtext)
			addtext = re.sub('<dl.*</dl>','',addtext.strip())
			# contains HTML?
			if (re.match('<.*>',addtext)):
				print("\t\tError: HTML in found text"+addtext)
			addtext = HTMLParser.HTMLParser().unescape(addtext)
		except:
			addtext = etree.tostring(div)
			addtext = re.sub('\n',' ',addtext)
			addtext = re.sub('<div class="detail_content">','',addtext)
			addtext = re.sub('<p>.*</div>','',addtext.strip())
			# contains HTML?
			if (re.match('<.*>',addtext)):
				print("\t\tError: HTML in found text"+addtext)
			addtext = HTMLParser.HTMLParser().unescape(addtext)
		content += addtext + ' '

		# content inside <p> tag
		paragraphs = root.findall("body/div/div/div/div/div[@class='entry-content']/div[@class='detail_content']/p")
		# consists of several paragraphs
		for p in paragraphs:
			if p.text is not None:
				content += p.text + ' '

		# get rid of multiple spaces
		headline = re.sub(' +',' ',headline.strip())
		teaser = re.sub(' +',' ',teaser.strip())
		content = re.sub(' +',' ',content.strip())

		# prepare JSON
		text_complete = teaser+" "+content

		nachricht = { "url": x, "headline": headline, "teaser": teaser, "content": content, "text" : text_complete, "time" : datetime.datetime.utcnow() }

		# write to mongo
		nachrichtenleicht.insert(nachricht)	

	# get all links from current page
	for a in root.iter("a"):
		if (a.get('href')):
			url = a.get('href')
			# if relative URL --> transform to absolute URL
			if (re.match('^/',url)):
				url = 'http://www.nachrichtenleicht.de'+url
			url = re.sub('/$','',url)
			# only add to set if the following conditions apply
			if (re.match('^http://www.nachrichtenleicht.de',url) # stay on site
					and not re.match('.*/attachment/.*|.*/wp-content/.*',url) # no non-HTML content
					and url not in visitedURLs): # not yet visited
				# update database
				if (url not in newURLs):
					visited.insert({ "url": x, "visited" : 0 })
				# update set-variable
				newURLs.add(url)

	# print count
	print("\t"+str(len(visitedURLs))+" URLs visited // "+str(len(newURLs))+" URLs to go.")
	return 0

def main():
	# starting point
	startURL = 'http://www.nachrichtenleicht.de/'
	startURL = re.sub('/$','',startURL)
	if startURL not in visitedURLs:
		newURLs.add(startURL)
	while (len(newURLs) > 0):
		# random delay
		time.sleep(random.randint(1,3))
		# start the crawling
		crawl(newURLs.pop())

	# finished
	print("\n")
	print("done. "+str(len(visitedURLs))+" URLs visited.")
	# close db connection
	con.disconnect()

	return 0

if __name__ == '__main__':
	main()
