#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

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
    if (len(word) != 3):
        continue
    if len(word[0]) == 1 or len(word[1]) == 1:
        continue
    if not re.match(pat,word[0]) or not re.match(pat,word[1]):
        continue
    if re.search(pat2,word[0]) or re.search(pat2,word[1]):
        continue
    if word[0] > word[1]:
        word[0], word[1] = word[1], word[0]
    newline = ','.join(word)
#    print(newline)
    coocs.add(newline)

for line in coocs:
    print(line)
