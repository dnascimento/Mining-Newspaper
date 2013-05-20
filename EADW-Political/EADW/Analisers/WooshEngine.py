#!/usr/bin/python
# -*- coding: utf-8 -*-
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser, OrGroup
from whoosh.writing import AsyncWriter
from collections import Counter
from operator import itemgetter, attrgetter
import os
import sqlite3
from setuptools.command.sdist import entities

###########################################################
# Whoosh engine
###########################################################
class WooshEngine:
    indexDir = "../storage/feedDir"
    
    def setDBName(self,dbName):
        self.dbName = dbName
    
    
    
    def createIndexDirIfNotExist(self):
        if os.path.exists(self.indexDir):
            return False
        os.makedirs(self.indexDir)
        print "    Directorio Criado"
        return True
    
              
    def addLink(self, url, title, summary, txt):
        
        titleb = title + " "
        title10 = titleb + titleb + titleb + titleb + titleb + titleb + titleb + titleb + titleb + titleb
        sumario = summary + " "
        sumario2 = sumario + sumario
        text = title10 + sumario2 + " " + txt
        
        ix = open_dir(self.indexDir, indexname='MAIN', readonly=False)
        writer = AsyncWriter(ix)
        writer.add_document(id=url, content=unicode(text)) 
        writer.commit()
        ix.close()
        # print "        Whoosh Added Titulo: " + title
    
    
    
    def createIndex(self):
        print "    Whoosh Loading from SQL "      
        created = self.createIndexDirIfNotExist()
        if not created:
            #already exists
            return
        
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute('''SELECT * FROM newsStorage where ARTICLE <> "" ''')
        feeds = c.fetchall()
        conn.close()
        
        linkN = 1
        schema = Schema(id = TEXT(stored = True), content=TEXT)
        ix = create_in(self.indexDir, schema, indexname='MAIN')
        writer = AsyncWriter(ix)

        for feed in feeds:
            
            # Descartar links sem Titulo
            if( isinstance(feed[3], type(None))):
                #print "is Null"
                continue
            
            index = feed[0]
            # print "    Whoosh Loaded Titulo " + str(linkN) + ":" + feed[3]
            linkN += 1
            
            titolo = feed[3] + " "
            titolo10 = titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo + titolo
            sumario = feed[4] + " "
            sumario2 = sumario + sumario
            text = titolo10 + sumario2 + " " +feed[5]
            
            writer.add_document(id=index, content=unicode(text))
            
            
        writer.commit()
        ix.close()   
        print "    Done Loading from SQL"
        # print "Whoosh Load End"
        
        
    def searchWord(self, word):
        if not os.path.exists(self.indexDir):
            print "Index must be created first"
            return
        
        ixD = open_dir(self.indexDir, indexname='MAIN', readonly=True)
        with ixD.searcher() as searcher:
            query = QueryParser("content", ixD.schema, group=OrGroup).parse(word.decode())
            #results = searcher.search(query, limit=None)
            results = searcher.search(query, limit=100)
            ixD.close()
            returnList = Counter()
            for i,r in enumerate(results):
                returnList += Counter({str(r.fields().values()[0]) : results.score(i)})
            return returnList
        
        
    def searchTop(self, word, maximum):
        res = self.searchWord(word).most_common(maximum)
        lista = []
        for result in res:
            lista.append([result[1], result[0]])
        return lista

    def searchTopWithEntity(self, word, maximum):
        res = self.searchWord(word).most_common(maximum)
        lista = []
        # pesquisar as entidades
        conn = sqlite3.connect(self.dbName)
        n = conn.cursor()
        for result in res:
            url = result[0]
            n.execute('''SELECT NAME, PRE_REPUTATION, REPUTATION
						FROM  newsStorage NATURAL JOIN opinion, personalities
						WHERE URL = ? AND  ENTITY = NAME
						ORDER BY PRE_REPUTATION DESC, REPUTATION DESC''', [url])
            ent = n.fetchall()
            entities = []
            # Limitar o numero de entidas a 5 por artigo
            for en in ent[:7]:
            	entities.append(en[0])
            #URL, SCORE, LISTA ENTIDADES
            lista.append([result[1], result[0], entities])
        conn.close()
        return lista
        

    def getMostFrequentWords(self):
        ixD = open_dir(self.indexDir, indexname='MAIN', readonly=True)
        reader = ixD.reader()
        whooshResult = reader.most_frequent_terms("content", number=100, prefix='')
        ixD.close()
         
        result = []
        for freq,val in whooshResult:
            if len(val) > 3:
                print str(freq)+":"+val
                result.append([freq,val])
            #TODO Taggar e ver se e nome

        return result
    
    
    def getMostFrequentCountries(self):
        countrySet = set()
        f = open("Utils/Personalites/input/paises.txt")
        for line in f:
            countrySet.add(unicode(line[:-1]).lower())
        
        ixD = open_dir(self.indexDir, indexname='MAIN', readonly=True)
        reader = ixD.reader()
        whooshResult = reader.most_frequent_terms("content", number=2000, prefix='')
        ixD.close()
        
        result = set()
        for freq,val in whooshResult:
            if len(val) > 3:
                try:
                    result.add(val.lower())
                except UnicodeEncodeError:
                    result.add(val.decode("utf-8").lower())
            
        result = countrySet.intersection(result)     
        
        final = []
        for country in result:
            for freq,val in whooshResult:
                if val == country:
                    final.append((country,int(freq)))
                    break
                
        final = sorted(final,key=lambda x: x[1],reverse=True)
        return final

