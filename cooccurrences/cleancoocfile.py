#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

# removes unwanted lines from a raw cooc file
try:
    infile = open(sys.argv[1])
except:
    print("error reading file / no file name given!")
    exit()

lines = infile.read().split('\n')
coocs = set()
pat = re.compile('[A-Za-z]')
pat2 = re.compile('\s')

for line in lines:
    word = line.split(',')
    # 'words' containing commas
    if (len(word) != 3):
        continue
    # 'words' of length 1
    if len(word[0]) == 1 or len(word[1]) == 1:
        continue
    # identical 'words'
    if word[0] == word[1]:
        continue
    # 'words' that are not words (i.e. not made of letters)
    if not re.match(pat,word[0]) or not re.match(pat,word[1]):
        continue
    # 'words' containing spaces
    if re.search(pat2,word[0]) or re.search(pat2,word[1]):
        continue
    # put words in lexical order to eliminate duplicate lines
    if word[0] > word[1]:
        word[0], word[1] = word[1], word[0]
    newline = ','.join(word)
    coocs.add(newline)

# print words to stdout
for line in coocs:
    print(line)
