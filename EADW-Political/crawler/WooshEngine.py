#!/usr/bin/python
# -*- coding: utf-8 -*-
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser, OrGroup
from collections import Counter
import os
import sqlite3


class WooshEngine:
    
    indexDir = "feedDir"
    dbName = ""
    
    def setDBName(self,dbName):
        self.dbName = dbName
    
    def __createIndexDir(self):
        if not os.path.exists(self.indexDir):
            os.makedirs(self.indexDir)
            print "Directory Created"
              
    def addLink(self, url, title, summary, txt):
        ix = open_dir(self.indexDir)
        writer = ix.writer()
        
        print "Titolo :" + title
        titolo = title + " "
        titolo10 = titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo
        sumario = summary + " "
        sumario2 = sumario + sumario
        text = titolo10 + sumario2 + " " + txt
        writer.add_document(id=url, content=unicode(text))
                  
        writer.commit()
        print "Added to Dir"
        
    def createEmptyIndex(self):
        self.__createIndexDir()
        schema = Schema(id = TEXT(stored = True), content=TEXT)
        ix = create_in(self.indexDir, schema)
    
    def createIndex(self, dbName):
        self.__createIndexDir()
        schema = Schema(id = TEXT(stored = True), content=TEXT)
        ix = create_in(self.indexDir, schema)
        writer = ix.writer()
        
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        print conn, dbName
        c.execute('''SELECT * FROM newsStorage''')
        feeds = c.fetchall()
        conn.close()
        
        linkN = 1
        for feed in feeds:
            index = feed[0]
            print "Titolo " + str(linkN) + ":" + feed[3]
            linkN += 1
            
            titolo = feed[3] + " "
            titolo10 = titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo
            sumario = feed[4] + " "
            sumario2 = sumario + sumario
            
            text = titolo10 + sumario2 + " " +feed[5]
            #print "Texto:"+ text
            writer.add_document(id=index, content=unicode(text))
                  
        writer.commit()
        print "Imported to Dir"
        
        
    def searchWord(self, word):
        if not os.path.exists(self.indexDir):
            print "Index must be created first"
            return
        
        ixD = open_dir(self.indexDir)
        with ixD.searcher() as searcher:
            query = QueryParser("content", ixD.schema, group=OrGroup).parse(word.decode())
            #results = searcher.search(query, limit=None)
            results = searcher.search(query, limit=100)
            
            returnList = Counter()
            for i,r in enumerate(results):
                returnList += Counter({str(r.fields().values()[0]) : results.score(i)})
            return returnList
        
        
    def searchTop(self, word, max):
        res = self.searchWord(word).most_common(max)
        list = []
        for result in res:
            list.append([result[1], result[0]])
        return list

    def searchTopWithEntity(self, word, max):
        res = self.searchWord(word).most_common(max)
        list = []
        # pesquisar as entidades
        conn = sqlite3.connect(self.dbName)
        n = conn.cursor()
        for result in res:
            url = result[0]
            n.execute('SELECT ENTITY FROM  newsStorage NATURAL JOIN opinion WHERE URL = ?', [url])
            entities = n.fetchall()
            list.append([result[1], result[0], entities])
        conn.close()
        return list
        
        
