#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
import re

def _remove_stopwords(sentence, stopwords):
    """
    input: sentence
    output: sentence with items also occurring in stopwords removed
    """
    return ' '.join(filter(lambda x: not x in stopwords, sentence.split()))

def _stem_sentence(stemmer, sentence):
    """
    input: sentence
    output: list of words in stemmed form
    """
    return ' '.join(map(stemmer.stem, sentence.split()))

def _clear_from_nonletters(text):
    return re.sub(r'[^a-zöäüß]+', ' ', text.lower())
   
def _parse_to_tokenized_sentences(tokenizer, text):
    text = re.sub(r'[.;:]+', '. ', text) # tokenizer does not recognize ';' and ':'. texts may contain multiple '.'s  
    return tokenizer.tokenize(text)

def preprocess(text, stem=True, remove_stopwords=True, language='german'):
    LANGUAGE = language
    STOPWORDS = stopwords.words(LANGUAGE)
    if LANGUAGE == 'german':
        STOPWORDS.append('dass') #not contained in stopwords
        
    sentences = _parse_to_tokenized_sentences(nltk.data.load('tokenizers/punkt/' + language + '.pickle'), text)
    
    if(remove_stopwords):
        sentences = map(_remove_stopwords, sentences)
    if(stem):
        sentences = _stem_sentence(SnowballStemmer(LANGUAGE), sentences)
    
    print("preprocessing finished") 
    return sentences
