#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import nltk, itertools, sys, math, getopt
from nltk.util import bigrams
from nltk.stem.snowball import GermanStemmer, EnglishStemmer
# correct encoding to use utf-8 everywhere
reload(sys)
sys.setdefaultencoding("UTF-8")
import preprocessing


def sentence_cooccurrence(tokenized_sentence):
    # returns a list of tuples. each word of the sentence is combined with each other word. first item is lexicographically smaller than second. list contains all occurences of all words (same combination may occure more than once).
    result = []
    index = 0
    while index < len(tokenized_sentence):
        index_2 = index+1
        while index_2 < len(tokenized_sentence):
            result.append((min(tokenized_sentence[index], tokenized_sentence[index_2]),max(tokenized_sentence[index], tokenized_sentence[index_2] )))
            index_2 += 1
        index += 1
    return result
    
def neighbour_cooccurrence(tokenized_sentence):
    result = []
    unsorted = bigrams(tokenized_sentence)
    for bg in unsorted:
        result.append((min(bg),max(bg)))
    return result

def create_wordcount_table(tokenlist):
    wordlist = {}
    for sentence in tokenlist:
        for word in sentence:
            if word in wordlist:
                wordlist[word] += 1
            else:
                wordlist[word] = 1
    return wordlist

def count_coocurrences(list_of_pairs):
    counts = {}
    for pair in list_of_pairs:
        if pair in counts:
            counts[pair] += 1
        else:
            counts[pair] = 1
    return counts

def sig_baseline(wa,wb, n_x_y, n_x, n):
    a = min(wa,wb)
    b = max(wa,wb)
    return n_x_y[(a,b)]

def sig_mutual_information(wa,wb, n_x_y, n_x, n):
    a = min(wa,wb)
    b = max(wa,wb)
    return math.log(float((n*n_x_y[(a,b)]))/(n_x[a]*n_x[b]))

def sig_dice(wa,wb, n_x_y, n_x, n):
    a = min(wa,wb)
    b = max(wa,wb)
    return 2*float(n_x_y[(a,b)])/(n_x[a]*n_x[b])

def sig_log(wa,wb, n_x_y, n_x, n):
    def _logfact(fact):
        return 0 if fact == 0 else fact * math.log(fact)
    a = min(wa,wb)
    b = max(wa,wb)

    fact_1 = n - n_x[a] - n_x[b] + n_x_y[(a,b)]
    fact_2 = n_x[a] - n_x_y[(a,b)]
    fact_3 = (n_x[b] - n_x_y[(a,b)]) 
    fact_4 = n - n_x[a] 
    fact_5 = n - n_x[b] 
    if fact_4 < 1: print fact_4
    
    return 2*(
        _logfact(n) - _logfact(n_x[a]) - _logfact(n_x[b]) + _logfact(n_x_y[(a,b)])
        + _logfact(fact_1)
        + _logfact(fact_2)
        + _logfact(fact_3)
        - _logfact(fact_4)
        - _logfact(fact_5))

class CooccurrenceCalculator:
    def __init__(self, filename, rem_stopwords=True, language='german'):
        stemmer = None
        if language == 'english': 
            stemmer = EnglishStemmer()
        else:
            stemmer = GermanStemmer()
        self.raw = preprocessing.preprocess(filename, stemmer, rem_stopwords, language )
        self.n = len(self.raw)
        
    def get_wordcount_table(self):
        if not hasattr(self, 'n_x'):
            self.n_x = create_wordcount_table(self.raw)    
        return self.n_x

    def get_neighbour_cooccurrences(self):
        if not hasattr(self, 'x_y_neighbour'):
            self.x_y_neighbour = map(neighbour_cooccurrence, self.raw)
        return self.x_y_neighbour

    def get_sentence_cooccurrences(self):
        if not hasattr(self, 'x_y_sentence'):
            self.x_y_sentence = map(sentence_cooccurrence, self.raw)
        return self.x_y_sentence

    def get_n_sentence_cooccurrences(self):
        if not hasattr(self, 'n_x_y_sentence'):
            self.n_x_y_sentence = count_coocurrences(list(itertools.chain.from_iterable(self.get_sentence_cooccurrences())))
        return self.n_x_y_sentence

    def get_n_neighbour_cooccurrences(self):
        if not hasattr(self, 'n_x_y_neighbour'):
            self.n_x_y_neighbour = count_coocurrences(list(itertools.chain.from_iterable(self.get_neighbour_cooccurrences())))
        return self.n_x_y_neighbour

    def get_significances(self, sig_function, n_x_y):
        sigs = {}
        for keytuple in n_x_y:
                if not keytuple in sigs and keytuple in n_x_y:
                    sigs[keytuple] = sig_function(keytuple[0], keytuple[1], n_x_y, self.get_wordcount_table(), self.n)
        return sigs




def print_sorted(the_dict):
    for w in sorted(the_dict, key=the_dict.get):
        print w, the_dict[w]


def write_to_file(the_dict, filename):
    f = open(filename, 'w')
    for w in sorted(the_dict, key=the_dict.get):
        f.write("\n" + w[0] + ", " + w[1] + " => " + str(the_dict[w])) 

def _run(infile, outfile, language, stem, remove_stopwords, neighbour, sig_func):
    calc = CooccurrenceCalculator(infile, remove_stopwords, language)
    if neighbour:
        write_to_file(calc.get_significances(sig_func, calc.get_n_neighbour_cooccurrences()), outfile)
    else:
        write_to_file(calc.get_significances(sig_func, calc.get_n_sentence_cooccurrences()), outfile)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    infile = ''
    outfile = ''
    language = 'german'
    stem = True
    remove_stopwords = True
    neighbour = False
    significance_function = sig_dice
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:o:l:nsf:S")
        except getopt.error, msg:
             raise Usage(msg)
        for o,a in opts:
            if o == '-i':
                infile = a
            elif o == '-o':
                outfile = a
            elif o == '-l':
                if not a in ['german', 'english']:
                    raise Usage("language may only be german or english")
                    return 2
                else:
                    language = a
            elif o == '-s':
                print "not stemming"
                stem = False
            elif o == '-S':
                print "not removing stopwords"
                remove_stopwords = False
            elif o == '-n':
                print "using neighbours"
                neighbour = True
            elif f == '-f':
                if a == 'MI':
                    significance_function = sig_mutual_information
                elif a == 'log':
                    significance_function = sig_log_likelihood
                elif a == 'base':
                    significance_function = sig_baseline
                elif a == 'dice':
                    significance_function = sig_dice
                else:
                    raise Usage("-f only accepts MI, log, base, or dice")
            elif o == '-h':
                print_help()
        if infile == '' or outfile == '': 
            print_help()
            return 2
    except Usage, err:
        print >>sys.stderr, err.msg
        return 2

    _run(infile, outfile, language, stem, remove_stopwords, neighbour, significance_function)


def print_help():
    print "Usage: -i inputfile -o outputfile [options] "
    print "options:"
    print "\t -l : language, may be german or english. Defaults to german"
    print "\t -s : do not stem"
    print "\t -S : do not remove stopwords"
    print "\t -n : use neighbour cooccurrence instead of sentence"
    print "\t -f [MI, log, base, dice] : choose the significance function. defaults to dice"

if __name__ == "__main__":
    sys.exit(main())











