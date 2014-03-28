#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
import nltk, itertools, codecs, sys, re
from nltk.stem.snowball import GermanStemmer


def _remove_stopwords(sentence):
    global STOPWORDS 
    def sw_filter(item):
        return not item.lower() in STOPWORDS
    return filter(sw_filter, sentence)

def _stem(stemmer, tokenlist):    
    def stem_sentence(sent):
        return map(stemmer.stem, sent)
    return map(stem_sentence, tokenlist) 

def _parse_to_tokenized_sentences(tokenizer, rawfile):
    rawfile = re.sub(re.compile(u'[.]+'), '. ', rawfile)
    tokenized = tokenizer.tokenize(rawfile)
    res = []
    for sentence in tokenized:
        sentence = re.sub(re.compile(u'[^a-z^A-Z^ä^ö^ü^Ä^Ö^Ü^ß]+'), ' ', sentence)
        res.append(sentence)
    return res

def _split(sentence_list):
    return map(unicode.split, sentence_list)

def preprocess(corpus, stemmer, remove_stopwords=True, language='german'):
    global STOPWORDS   
    LANGUAGE = language
    STOPWORDS = map(unicode, stopwords.words(LANGUAGE))
    STOPWORDS.append(u'dass') #not contained in stopwords
    sentence_list = _parse_to_tokenized_sentences(nltk.data.load('tokenizers/punkt/' + language + '.pickle'), corpus)
    sentences = _split(sentence_list)
    #for s in sentence_list:
    #    print s
    if(remove_stopwords): sentences = map(_remove_stopwords, sentences)
    if(stemmer is not None): sentences = _stem(stemmer, sentences)
    print "preprocessing finished" 
    return sentences
