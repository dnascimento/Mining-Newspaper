#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.corpus import mac_morpho
import re
import unicodedata
import os
import sqlite3

class TAGAnalizer:
    TagDBPath = "../storage/lexicon.db"     
    
    def __init__(self):
        # Liga a BD
        self.conn = sqlite3.connect(self.TagDBPath)     
        self.c = self.conn.cursor()
    
    def loadDictionary(self,Filename):
        list = []
        f = open(Filename, "r")
        for line in f:
            key = line.split(":")[0]
            value = line.split(":")[1]
            if(len(line.split(":"))>2):
                value = line.split(":")[2]
            if('\n' in value):
                value = value.split('\n')[0]
            list.append([key, value])
        f.close()
        return dict(list)
    
    # devolve o valor da tag a partir da BD           
    def getTagFromBD(self, word):
        #Normalize
        word = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))
        
        self.c.execute('SELECT POS FROM lexicon WHERE WORD = ?', [word])
        result = self.c.fetchone()
        
        if(isinstance(result, type(None))):
            return str(unicode('null'))
        else:
            return result[0]                

