#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import nltk, itertools, sys, math, getopt, os,codecs, json
from nltk.util import bigrams
from nltk.stem.snowball import GermanStemmer, EnglishStemmer
from py2neo import neo4j
from pymongo import MongoClient
# correct encoding to use utf-8 everywhere
reload(sys)
sys.setdefaultencoding("UTF-8")
import preprocessing


def sentence_cooccurrence(tokenized_sentence):
    # returns a list of tuples. each word of the sentence is combined with each other word. first item is lexicographically smaller than second. list contains all occurences of all words.
    result = []
    index = 0
    while index < len(tokenized_sentence):
        index_2 = index+1
        while index_2 < len(tokenized_sentence):
            duo = (min(tokenized_sentence[index], tokenized_sentence[index_2]),max(tokenized_sentence[index], tokenized_sentence[index_2] ))
            if result.count(duo) == 0:
                result.append(duo)
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
        # <= weil bei sätzen wie [...] Ai Weiwei Ai Weiwei [...] (in dem Beispiel wurden im original versehentlich die Sätze nicht getrennt) die Kookkurrenz (ai, weiwei) drei mal vorkommt die wörter aber je nur zwei mal
        if fact <= 0:
            return 0
        else:
            return fact * math.log(fact)
    a = min(wa,wb)
    b = max(wa,wb)

    _A = n_x_y[(a,b)]
    _B = n_x[a]-n_x_y[(a,b)]
    _C = n_x[b]-n_x_y[(a,b)]
    _D = n - n_x[a] - n_x[b]

    return 2*(_logfact(_A)
        + _logfact(_B)
        + _logfact(_C)
        + _logfact(_D)
        - _logfact((_A+_B))
        - _logfact((_A+_C))
        - _logfact((_B+_D))
        - _logfact((_C+_D))
        + _logfact((_A+_B+_C+_D)))


class CooccurrenceCalculator:
    def __init__(self, corpus, stem, rem_stopwords=True, language='german'):        
        stemmer = None
        if stem and language == 'english': 
            stemmer = EnglishStemmer()
        elif stem and language == 'german':
            stemmer = GermanStemmer()
        self.raw = preprocessing.preprocess(corpus, stemmer, rem_stopwords, language )
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

def write_to_file(the_dict, wordlist, filename):
    # writes the cooccurrences to a csv file (word, word, value)
    f = open(filename, 'w')
    for w in sorted(the_dict, key=the_dict.get):
        f.write(w[0] + ", " + w[1] + ", " + str(the_dict[w]) + "\n") 

def write_geoff_file(the_dict, wordlist, filename):
    # doesn't use the _convert_to_geoff method to prevent using the needed memory by writing line by line directly to file.
    f = open(filename, 'w')
    for w in wordlist:
        f.write(''.join(["(", w.title(), ':Word { word:"', w, '"})\n']))
    for rel in sorted(the_dict, key=the_dict.get):
        f.write(''.join(["(", rel[0].title(), ")-[:OCCURS_WITH { value: ", "{:.20f}".format(the_dict[rel]), "}]->(", rel[1].title(), ")\n"])) 

def _convert_to_geoff(the_dict, wordlist):
    geoff = ''
    for w in wordlist:
        geoff = ''.join([geoff, "(", w.title(), ':Word { word:"', w, '"})\n'])
    for rel in sorted(the_dict, key=the_dict.get):
        geoff = ''.join([geoff, "(", rel[0].title(), ")-[:OCCURS_WITH { value: ", "{:.20f}".format(the_dict[rel]), "}]->(", rel[1].title(), ")\n"])
    return geoff 

def write_to_neo4j(the_dict, wordlist, filename):
    # first changes the data into the geoff format so that nodes have a variable name for the transaction and then writes it to the neo4j database. be sure the server is running! also this cleans the complete db.
    graph_db = neo4j.GraphDatabaseService()
    graph_db.clear()
    print("db cleared")
    print("loading geoff")
    graph_db.load_geoff(_convert_to_geoff(the_dict, wordlist))
    print("db filled")

def _read_from_mongo(url):
    url = url.split('/')
    con = MongoClient(url[0])
    db = con[url[1]][url[2]]
    corpus = "" 
    # get text from database (one line = one article)
    for row in db.find():
        corpus = corpus + row['text']
    print corpus
    return corpus

# helper method up to now only used in REPL
def dump_db_as_asv_source(url, filename):
    # read from db
    url = url.split('/')
    con = MongoClient(url[0])
    db = con[url[1]][url[2]]
    corpus = []
    # get text from database (one line = one article)
    
    # write to file
    with open(filename, 'w') as f:
        for row in db.find():
            item = {'text': row['text'], 'url': row['url']}
            f.write( ''.join(['<source><location>', item['url'], '</location></source>\n', item['text'], '\n'])) 
    return 

def _run(infile, outfile, language, stem, remove_stopwords, neighbour, sig_func, mode):
    if mode == 'db':
        method = write_to_neo4j
        corpus = _read_from_mongo(infile)
    elif mode == 'geoff' :
        method = write_geoff_file
        corpus = codecs.open(infile, encoding='utf-8').read()
    elif mode == 'csv':
        method = write_to_file
        corpus = codecs.open(infile, encoding='utf-8').read()

    calc = CooccurrenceCalculator(corpus, stem, remove_stopwords, language)

    if neighbour:
        method(calc.get_significances(sig_func, calc.get_n_neighbour_cooccurrences()),  calc.get_wordcount_table().keys(), outfile)
    else:
        method(calc.get_significances(sig_func, calc.get_n_sentence_cooccurrences()), calc.get_wordcount_table().keys(), outfile)


   


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
    mode = "geoff"
    significance_function = sig_log
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:o:l:nsf:Sm:")
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
            elif o == '-f':
                if a == 'MI':
                    significance_function = sig_mutual_information
                elif a == 'log':
                    significance_function = sig_log
                elif a == 'base':
                    significance_function = sig_baseline
                elif a == 'dice':
                    significance_function = sig_dice
                else:
                    raise Usage("-f only accepts MI, log, base, or dice")
            elif o == '-h':
                print_help()
                exit()
            elif o == '-m':
                if not a in ['geoff', 'csv', 'db']:
                    raise Usage("modes may only be [db, geoff, csv]")
                    return 2
                mode = a
        if infile == '' or outfile == '': 
            print_help()
            return 2
    except Usage, err:
        print >>sys.stderr, err.msg
        return 2

    _run(infile, outfile, language, stem, remove_stopwords, neighbour, significance_function, mode)


def print_help():
    print "Usage: -i inputfile -o outputfile [options] "
    print "options:"
    print "\t -l : language, may be german or english. Defaults to german"
    print "\t -s : do not stem"
    print "\t -S : do not remove stopwords"
    print "\t -n : use neighbour cooccurrence instead of sentence"
    print "\t -f [MI, log, base, dice] : choose the significance function.defaults to log"
    print "\t -m [db, csv, geoff]: set mode. in db mode use -i for input url (mongodb) and -o for the output neo4j url. otherwise use filenames. default to geoff"

if __name__ == "__main__":
    sys.exit(main())











