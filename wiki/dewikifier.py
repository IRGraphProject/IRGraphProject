#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import codecs
import re
import pymongo
import HTMLParser
from itertools import imap
import mwparserfromhell

con = pymongo.Connection('127.0.0.1', port=27017)
wiki = con.wikidb.dump
# clear data collection (if exists)
wiki.drop()

f = codecs.open('pages.json', encoding='utf-8')

for line in f:

    try:
        pageset = json.loads(line[:-2])
    except:
        print "X"
        continue;
        
    blacklist = ['redirect']
    if ( pageset['english'] and pageset['simple'] and
        all(substr not in pageset['english'].lower() for substr in blacklist) and
        all(substr not in pageset['simple'].lower() for substr in blacklist)):

        epage = mwparserfromhell.parse(pageset['english'])
        spage = mwparserfromhell.parse(pageset['simple'])
        wle = epage.filter_wikilinks()
        wls = spage.filter_wikilinks()

        for wl in wle:
            if '[[Category' in wl:
                try:
                    epage.remove(wl)
                except:
                    print "removal failed"
        for wl in wls:
            if '[[Category' in wl:
                try:
                    spage.remove(wl)
                except:
                    print "removal failed"

        epage = epage.strip_code(normalize=True, collapse=True)
        spage = spage.strip_code(normalize=True, collapse=True)

        i = 0
        while "{|" in epage and "|}" in epage and i < 1000:
            start = epage.find("{|")
            end = epage.find("|}", start)
            epage = epage[:start] + epage[end+2:]
            i = i + 1

        i = 0
        while "{|" in spage and "|}" in spage and i < 1000:
            start = spage.find("{|")
            end = spage.find("|}", start)
            spage = spage[:start] + spage[end+2:]
            i = i + 1

        if len(spage)>0 and len(epage)>0:
            print "*"
            stripset = {}
            stripset['simple'] = spage
            stripset['english'] = epage
            stripset['title'] = pageset['title']
            wiki.save(stripset)
        else:
            print "X"
