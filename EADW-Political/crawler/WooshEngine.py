#!/usr/bin/python
# -*- coding: utf-8 -*-
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, NUMERIC, TEXT
from whoosh.qparser import QueryParser, OrGroup
from collections import Counter
import os
import sqlite3


class WooshEngine:
    
    fileToIntex = ""
    indexDir = "feedDir"
    dbName = ""
    
    def __init__(self, fileToIndex, dbName):
        self.fileToIntex = fileToIndex
        self.dbName = dbName;


    def __createIndexDir(self):
        if not os.path.exists(self.indexDir):
            os.makedirs(self.indexDir)
            print "Directory Created"
              
                
    def createIndex(self):
        self.__createIndexDir()
        schema = Schema(id = NUMERIC(stored=True), content=TEXT)
        ix = create_in(self.indexDir, schema)
        writer = ix.writer()
        
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        print conn, self.dbName
        c.execute('''SELECT * FROM newsStorage''')
        feeds = c.fetchone()
        print feeds
        conn.close()
        
        for feed in feeds:
            print feed
        
        #writer.add_document(id=index, content=unicode(text))
        #print index, text
                  
        #fecha FD
        #fileDesc.close()
        #writer.commit()
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

engine = WooshEngine("cenas", "news.db")
engine.createIndex()
print engine.searchWord("cenas")

