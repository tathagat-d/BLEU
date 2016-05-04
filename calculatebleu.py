#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import string
import glob

if len(sys.argv) != 3:
    exit(0)

#==========================================================#
outFile= open('bleu_out.txt', 'w')
#==========================================================#

#==========================================================#
candidate = sys.argv[1]
candidateHand = open(candidate, 'r')
#==========================================================#

#==========================================================#
reference = sys.argv[2]
if os.path.isdir(reference):
    if sys.argv[2].endswith('/'):
        docs = glob.glob(reference + '*.txt')
    else:
        docs = glob.glob(reference + '/*.txt')
else:
    docs = list()
    docs.append(reference)

reference = dict()
for doc in docs:
    reference[doc] = open(doc, 'r')
#==========================================================#
# Beginning of clean_text
def clean_text(text):
    ''' Doing what string.translate should do '''  
    text=text.replace(u"।", '')
    text=text.replace(u'\\','')
    text=text.replace(u'!','')
    text=text.replace(u'@','')
    text=text.replace(u',','')
    text=text.replace(u'"','')
    text=text.replace(u'(','')
    text=text.replace(u')','')
    text=text.replace(u'"','')
    text=text.replace(u"'",'')
    text=text.replace(u"‘‘",'')
    text=text.replace(u"’’",'')
    text=text.replace(u"''",'')
    text=text.replace(u".",'')
    text=text.replace(u":",'')
    text=text.replace(u"-",'')
    text=text.replace(u"?",'')
    text=text.replace(u"  ",' ')
    return text
# End of clean text
#==========================================================#

#============================================================#
def computeGram1(line):
    freq = dict()
    line = line.split()
    denominator = len(line)
    unique = list(set(line))
    #========================================================#
    for doc in docs:
        ref = reference[doc].readline()
        ref = ref.strip().decode('utf-8', 'ignore')
        ref = clean_text(ref)
        ref = ref.split()
        #====================================================#
        for word in unique:
            match = min(line.count(word), ref.count(word))
            if not word in freq:
                freq[word] = match
            elif freq[word] < match:
                freq[word] = match
        #====================================================#
    #========================================================#
    return float(sum(freq.values()))/denominator
#============================================================#

weight = 0.25
# Processing Step
for line in candidateHand:
    line = line.strip().decode('utf-8', 'ignore')
    line = clean_text(line)
    p1   = computeGram1(line)
    break
#==========================================================#
outFile.close()
candidateHand.close()
for fhand in reference.values():
    fhand.close()
#==========================================================#
