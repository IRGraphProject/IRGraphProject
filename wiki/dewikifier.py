#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import codecs
import re
import pymongo
import HTMLParser
from itertools import imap
import mwparserfromhell


def remove_links(page):
    # fetch a list of wiki links
    wls = page.filter_wikilinks()
    # filter out Category links
    for wl in wls:
        if '[[Category' in wl:
            try:
                page.remove(wl)
            except:
                print "removal failed"

def remove_headings(page):
    # fetch a list of wiki headings
    whs = page.filter_headings()
    # filter out headings
    for wh in whs:
        page.remove(wh)

def remove_lists(page):
    for line in page.split('\n'):
        if re.match('[*#;:].*', line):
            try:
                page.remove(line, recursive=True)
            except:
                # removal 'fails' but for some reason content isn't there
                # anymore anyway
                pass

def remove_tables(page):
    while True:
        try:
            start = page.index('{|')
            end = page.index('|}')
            page = page.remove(page[start:end+2])
        except:
            break
        

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
    # Don't add redirect pages 
    if ( pageset['english'] and pageset['simple'] and
        all(substr not in pageset['english'].lower() for substr in blacklist) and
        all(substr not in pageset['simple'].lower() for substr in blacklist)):

        spage = mwparserfromhell.parse(pageset['simple'])
        epage = mwparserfromhell.parse(pageset['english'])

        remove_lists(epage)
        remove_lists(spage)

        remove_headings(epage)
        remove_headings(spage)

        remove_links(epage)
        remove_links(spage)

        remove_tables(epage)
        remove_tables(spage)

        # remove remaining mediawiki tags
        epage = epage.strip_code(normalize=True, collapse=True)
        spage = spage.strip_code(normalize=True, collapse=True)

        # write to data base
        if len(spage)>0 and len(epage)>0:
            print "*"
            stripset = {}
            stripset['simple'] = spage
            stripset['english'] = epage
            stripset['title'] = pageset['title']
            wiki.save(stripset)
        else:
            print "X"
        del spage
        del epage
        del pageset

