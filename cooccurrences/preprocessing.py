#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
import nltk, itertools, codecs, sys
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
    # use
    tokenized = tokenizer.tokenize(rawfile)
    res = []
    for sentence in tokenized:
        sentence = sentence.replace('.', ' ')
        sentence = sentence.replace(',', ' ')
        sentence = sentence.replace('?', ' ')
        sentence = sentence.replace('!', ' ')
        res.append(sentence)
    return res

def _split(sentence_list):
    return map(unicode.split, sentence_list)

def preprocess(filepath, stemmer, remove_stopwords=True, language='german'):
    global STOPWORDS   
    LANGUAGE = language
    STOPWORDS = map(unicode, stopwords.words(LANGUAGE))
    STOPWORDS.append(u'dass') #not contained in stopwords

    f = codecs.open(filepath, encoding='utf-8')
    raw = f.read()
    sentence_list = _parse_to_tokenized_sentences(nltk.data.load('tokenizers/punkt/' + language + '.pickle'), raw)
    sentences = _split(sentence_list)
    if(remove_stopwords): sentences = map(_remove_stopwords, sentences)
    if(stemmer is not None): sentences = _stem(stemmer, sentences)
    return sentences
