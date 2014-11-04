#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  crop wikipedia articles to the same length and write them to files

import json
import pymongo
import re
import nltk
import codecs

con = pymongo.Connection('localhost', port=27017)
wiki = con.wikidb.dump

# files
file_en = codecs.open("../data/wiki_english_source.txt","w","utf-8") # english
file_sim = codecs.open("../data/wiki_simple_source.txt","w","utf-8") # simple english
file_titles = codecs.open("../data/wiki_titles_source.txt","w","utf-8") # debug

tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

# remove linebreaks, headings, lists etc. from the text - keep only sentences
def get_sentences(x):
    sentences = []
    
    # split into lines
    lines = x.splitlines()
    for line in lines:
        line = line.strip() # remove whitespaces
        if not line == "": # skip empty lines
            if line.endswith('.') | line.endswith('!') | line.endswith('?'): # if line ends with 
#                print "line: "+line
                tokens = tokenizer.tokenize(line) # split into sentences
                for token in tokens:
                    sentences.append(token)
    return sentences

# main function
def main():
    for row in wiki.find():

        title = row['title']
        file_titles.write(title + '\n')
        # get sentences for english
        english = row['english']
        sentences_en = get_sentences(english)
        # ... and simple english wikipedia
        simple = row['simple']
        sentences_sim = get_sentences(simple)
        # lengths
        len_en = len(sentences_en)
        len_sim = len(sentences_sim)

        # compare lengths
        if len_en > len_sim: # english longer
            sentences_en = sentences_en[0:len_sim] # crop english
        elif len_en < len_sim: # simple longer
            sentences_sim = sentences_en[0:len_sim]    # crop simple
        print "en: "+str(len_en)+" / sim: "+str(len_sim)+ " / cropped to "+str(min(len_en,len_sim))+" / title: "+title

        # save titles/locations
        if (min(len_en,len_sim)):
            # english
            file_en.write("<source><location>http://en.wikipedia.org/wiki/"+title+"</location></source>\n")
            # simple english
            file_sim.write("<source><location>http://simple.wikipedia.org/wiki/"+title+"</location></source>\n")
        
        # write remaining sentences to file (one sentence per line)
        # english
        for s in sentences_en:
    #        print "\t"+s
            file_en.write(s + '\n')
        # simple english
        for s in sentences_sim:
    #        print "\t"+s
            file_sim.write(s + '\n')


    #finish
    file_en.close()
    file_sim.close()
    file_titles.close()

    con.disconnect()
    return 0

if __name__ == '__main__':
    main()
