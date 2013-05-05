#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.corpus import mac_morpho
import re
import unicodedata
import os
import sqlite3

class TAGAnalizer:
    TagDBPath = "../storage/lexicon.db"     
    TagFile = "Utils/SentimentsBase/in/TagFile.txt"    
    
    def __init__(self):
        self.loadToDB()
    
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
    
    
    def loadToDB(self):
        # Apag BD antiga
        conn = sqlite3.connect(self.TagDBPath)
        c = conn.cursor()
        c.execute('DELETE FROM tags')
        conn.commit()       
        # Carega o ficheiro para a BD
        fd = open(self.TagFile, 'r')
        for line in fd:
            word = line.split(":")[0]
            tag  = line.split(":")[1].split("\n")[0]
            
            if '|' in tag:
                tag = tag.split('|')[0]
                
            # Normalize
            word = unicode(word).lower() 
            tag = unicode(tag)
            
            #Apenas precisamos destes
            if (tag != 'NPROP' and tag != 'ADJ'):
				continue
            
            try:
                c.execute('Insert into tags(WORD,TAG) values(?,?)',(word,tag))
            except sqlite3.IntegrityError:
                if(tag == 'NPROP'):
                    c.execute('UPDATE tags set TAG = ? WHERE WORD = ?',(tag,word))
                pass
                
        # Fecha Coneccoes
        conn.commit()
        conn.close() 
        fd.close()
        
    
    # devolve o valor da tag a partir da BD           
    def getTagFromBD(self, word):
        #Normalize
        conn = sqlite3.connect(self.TagDBPath)  
        c = conn.cursor()   
        word = unicode(word).lower()
        
        c.execute('SELECT TAG FROM tags WHERE WORD = ?', [word])
        result = c.fetchone()
        
        conn.close()
        if(isinstance(result, type(None))):
            return str(unicode('null'))
        else:
            return result[0]                

