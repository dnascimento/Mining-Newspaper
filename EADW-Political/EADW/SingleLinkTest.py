#!/usr/bin/env python
# -*- coding: utf-8 -*-
from EADW.Analisers.TAGAnalizer import TAGAnalizer
from collections import Counter
from EADW.Downloaders.ContentDownloader import ContentDownloader
from threading import Thread
import sqlite3, nltk, string, unicodedata

def strip_punctuation(text):
        punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
        return ''.join(x for x in text if unicodedata.category(x) not in punctutation_cats)
       
link = "http://sol.sapo.pt/inicio/Sociedade/Interior.aspx?content_id=74326"

counter = Counter()
toRemovetList= []
cntdown = ContentDownloader("")
tag = TAGAnalizer()
simpleIgnoreList = ["da", "do", "das",]

text = cntdown.parseSite(link,"",1)
if text is None:
    print "Link Error"
    print text
    
sentences = nltk.sent_tokenize(text.decode("utf8"))

for sentence in sentences:
    
    sentence = strip_punctuation(sentence)
    words = sentence.split(" ")
    print words
    for word in words:
        
        #encontra lixo
        if(len(word) < 2):
            continue
           
        if(word in simpleIgnoreList):
        	continue
                        
        POS = tag.getTagFromBD(word)
        print word, POS
        if  POS == 'NPROP':
            print "-----------------> ",word
            
