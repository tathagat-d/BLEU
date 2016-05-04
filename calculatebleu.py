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
def getBigram(words):
    temp = list()
    for i in range(len(words) - 1):
        temp.append(words[i] + u' ' + words[i+1])
    return temp
#=======================================================================#
def getTrigram(words):
    temp = list()
    for i in range(len(words) - 2):
        temp.append(words[i] + u' ' + words[i + 1] + u' ' + words[i + 2])
    return temp
#=======================================================================#
def getQuadgram(words):
    temp = list()
    for i in range(len(words) - 3):
        temp.append(words[i] + u' ' + words[i + 1] + u' ' + words[i + 2] + u' ' + words[i + 3])
    return temp
#=======================================================================#
def getFreq(freq, unique, line, ref):
    for word in unique:
        match = min(line.count(word), ref.count(word))
        if not word in freq:
            freq[word] = match
        elif freq[word] < match:
            freq[word] = match
    return freq
#=============================================================#
def computeGram(line):
    freq, freq2, freq3, freq4 = dict(), dict(), dict(), dict()
    # For UNIGRAM
    line = line.split()
    unique = list(set(line))
    denominator = len(line)
    # For BIGRAM
    line2= getBigram(line)
    denominator2 = len(line2)
    unique2 = list(set(line2))
    # For TRIGRAM
    line3= getTrigram(line)
    denominator3 = len(line3)
    unique3 = list(set(line3))
    # For QUADGRAM
    line4 = getQuadgram(line)
    denominator4 = len(line4)
    unique4 = list(set(line4))
    #========================================================#
    for doc in docs:
        ref = reference[doc].readline()
        ref = ref.strip().decode('utf-8', 'ignore')
        ref = clean_text(ref)
        ref = ref.split()
        #====================================================#
        # UNIGRAM
        getFreq(freq, unique, line, ref)
        p1 = float(sum(freq.values()))/denominator
        #====================================================#
        # BI-GRAM
        ref2 = getBigram(ref)
        getFreq(freq2, unique2, line2, ref2)
        p2 = float(sum(freq2.values()))/denominator2
        #====================================================#
        # TRI-GRAM
        ref3 = getTrigram(ref)
        getFreq(freq3, unique3, line3, ref3)
        p3 = float(sum(freq3.values()))/denominator3
        #====================================================#
        # QUAD-GRAM
        ref4 = getQuadgram(ref)
        getFreq(freq4, unique4, line4, ref4)
        p4 = float(sum(freq4.values()))/denominator4
    #========================================================#
    return p1, p2, p3, p4
#============================================================#

weight = 0.25
# Processing Step
for line in candidateHand:
    line = line.strip().decode('utf-8', 'ignore')
    line = clean_text(line)
    p1, p2, p3, p4   = computeGram(line)
    print p1, p2, p3, p4
#==========================================================#
outFile.close()
candidateHand.close()
for fhand in reference.values():
    fhand.close()
#==========================================================#
