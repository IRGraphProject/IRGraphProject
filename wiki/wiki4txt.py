#!/usr/bin/python
# -*- coding: utf-8 -*-

# remove mediawiki markup from article and return plaintext
#

import json
import codecs
import re
import regex
import pymongo
import pprint

# removes wiki categories
def remove_categories(line):
    # filter out Category links
    line = re.sub("\[\[Category:.*?\]\]","",line)
    return line

# remove redirects
def remove_redirects(page):
    page = re.sub("\#REDIRECT \[\[.*\]\]","",page)
    return page

# remove headings because they're not sentences
def remove_headings(line):
    line = re.sub("==+.*?==+","",line)
    return line

# remove lists because they're not sentences either
def remove_lists(page):
    container = page.split('\n')
    newpage = u""
    for line in container:
#        print (line)
        if not re.match('^\s*[\*\#\;\:]', line):
#            print ("OK:" + line)
            newpage += line + "\\n"
#        else:
#            print ("***REMOVED: "+line)
    return newpage

# remove tables
def remove_tables(page):
    p = re.compile("\{\|.*?\|\}",re.DOTALL)
    page = re.sub(p,"<table />",page)
    return page

# remove stuff in <> angled brackets
def remove_angledbrackets(line):
	line = re.sub("<.*?>","",line)
	return line

# remove stuff in curly brackets (including nested)
def remove_curlybrackets(pre, line):
#	print "----"
	while line.find('{{') > -1:
		start = line.find('{{')
		end = line.find('}}')

		before = line[:start+2] #what's before {{
		rest = line[start+2:]	#what's behind

		start2 = rest.find('{{')
		end2 = rest.find('}}')

		if end2 < start2 or start2 == -1 : #no nested structure
			removed = line[start:end+2]
#			print "\nremoving: "+removed
			line = line[0:start] + line[end+2:]
			if line.find('{{') == -1 or removed == '':
				break
		else: #nested structure; entering recursion
			line = remove_curlybrackets(before,rest)
	return pre + line

# remove wiki links [[...]]
def remove_wikilinks(page):
    # step 1: replace link with title
    page = regex.sub(r"(?r)\[\[.*?\|","[[",page)
    page = re.sub(r"\[\[","",page)
    page = re.sub(r"\]\]","",page)
    return page

# remove external links [http://...]
def remove_links(page):
    # step 1: replace link with title
    page = p.sub(r"\1", page)
    page = re.sub("\[.*?\]","",page)
    return page

# remove non-breaking spaces
def remove_spaces(page):
    # remove html spaces
    page = re.sub(r"&nbsp;"," ",page)
    # remove linebreaks
    page = re.sub(r"\\n"," ",page)
    # remove multiple spaces
    page = re.sub(r"\s+"," ",page)
    page = page.strip()
    return page

def main():
    p = re.compile('\[http.*? (.*?)\]')

    con = pymongo.Connection('127.0.0.1', port=27017)
    wiki = con.wikidb.dump
    # clear collection (if exists)
    wiki.drop()

    f = codecs.open('../data/pages.json', encoding='utf-8')
    #f = codecs.open('../data/page_one.txt', encoding='utf-8')
    #f = codecs.open('../data/phead.json', encoding='utf-8')

    linecount = 0

    for line in f:
        linecount += 1
        if (linecount % 1000 == 0):
            print str(linecount) + " done"
        # handle as JSON
        try:
            jline = json.loads(line[:-2])

            # remove redirect pages and pages available only in one language
            blacklist = ['redirect']
            if ( jline['english'] and jline['simple'] and
                all(substr not in jline['english'].lower() for substr in blacklist) and
                all(substr not in jline['simple'].lower() for substr in blacklist)):

                # do stuff for simple
                sim = jline['simple']
                sim = remove_categories(sim)
                sim = remove_redirects(sim)
                sim = remove_headings(sim)
                sim = remove_lists(sim)
                sim = remove_tables(sim)
                sim = remove_curlybrackets('',sim)
                sim = remove_angledbrackets(sim)
                sim = remove_wikilinks(sim)
                sim = remove_links(sim)
                sim = remove_spaces(sim)
    #            print sim

                # do stuff for english
                eng = jline['english']
                eng = remove_categories(eng)
                eng = remove_redirects(eng)
                eng = remove_headings(eng)
                eng = remove_lists(eng)
                eng = remove_tables(eng)
                eng = remove_curlybrackets('',eng)
                eng = remove_angledbrackets(eng)
                eng = remove_wikilinks(eng)
                eng = remove_links(eng)
                eng = remove_spaces(eng)
    #           print eng

                # new JSON object
                newline = {}
                newline['title'] = jline['title']
                newline['simple'] = sim
                newline['english'] = eng

#                print(newline)

                # save to database
                wiki.insert(newline)
    #        else:
    #            print "blacklisted for redirect: " + jline['title']
        except:
            print "JSON load failed for "+line
            continue;

    return 0

if __name__ == '__main__':
    main()
