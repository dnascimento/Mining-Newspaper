#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from bs4 import BeautifulSoup
from sqlite3 import OperationalError
from EADW.Analisers.WooshEngine import WooshEngine
from bs4 import UnicodeDammit
import urllib, os, hashlib
import re, sys, sqlite3, chardet, urllib
from EADW.Analisers import EntityExtract

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database   
class ContentDownloader(Thread):
    
    __dbName = ""
    whoosh = ""
    __dBEntitiesLocation = "../storage/lexicon.db"
    TMPpath = "../storage/tmp/"
    Narticles = 0
    
    
    def __init__(self,dbName):
        Thread.__init__(self)
        self.__dbName = dbName
        self.entityExtraction = EntityExtract.EntityExtractor()
        self.whoosh = WooshEngine()
    
    #Read from DB each entry with: url and Date
    def start(self):
        self.__conn = sqlite3.connect(self.__dbName)     
        self.__cursor = self.__conn.cursor()   
        print "Download Content Start"
        #Take a pendent processing elements snapshot
        i = 0
        newsList = []
        for row in self.__cursor.execute("Select * from newsStorage where PROCESSED='False'"):
            newsList.append([row[0],row[1]])
              
        for news in newsList:
            self.parseSite(news[0],news[1])
     
        

    ######################################################
    #####  Download site content and store it on database
    ######################################################
    def parseSite(self,url,date,justDownload=0):
        
        doc = ""
        title = ""
        summary = ""
        article = ""
        # Verificar se o ficheiro já existe em Cache
        #Caso nao vamos tb guardalo em cache
        if not os.path.exists(self.TMPpath+hashlib.sha1(url).hexdigest()+".txt"):
            fileURL = urllib.urlopen(url)
            doc = fileURL.read()
            f = open(self.TMPpath+hashlib.sha1(url).hexdigest()+".txt", "w+")
            f.write(doc)
            f.flush()
            f.close()
        
        # Se existir vamos caregalo do disco
        else:
            f = open(self.TMPpath+hashlib.sha1(url).hexdigest()+".txt", "r")
            doc = f.read()
            f.close()

        
        domain = re.split("http://",url)[1]   
        domain = re.split("\.pt|\.com",domain)[0]
            
            
        soup = BeautifulSoup(doc)
        #print soup.original_encoding
        try:
            if domain == "expresso.sapo":
                title = unicode(soup.select("#artigo")[0].h1.get_text().encode("utf8"))
                summary = unicode(soup.select("#artigo")[0].summary.get_text().encode("utf8"))
                article =  unicode(soup.select("#conteudo")[0].get_text().encode("utf8"))
            
            if domain == "feeds.dn":
                title = unicode(soup.select("#NewsTitle")[0].get_text().encode("utf8"))
                summary = unicode(soup.select("#NewsSummary")[0].get_text().encode("utf8"))
                article = unicode(soup.select("#Article")[0].get_text().encode("utf8"))
            
            #N
            #if domain == "rss.feedsportal":
            #    title = unicode(soup.select("#NewsTitle")[0].get_text().encode("utf8"))
            #    summary = unicode(soup.select("#NewsSummary")[0].get_text().encode("utf8"))
            #    article = unicode(soup.select("#Article")[0].get_text().encode("utf8"))
            
            
            if domain == "economico.sapo":
                title = unicode(soup.select(".meta")[0].h2.get_text().encode("utf8"))
                summary = unicode(soup.select(".mainText")[0].strong.get_text().encode("utf8"))
                article = unicode(soup.select(".mainText")[0].get_text().encode("utf8"))
            
            #N
            #if domain == "www.sol" or domain == "sol.sapo":
            #    title = unicode(soup.select("#NewsTitle")[0].get_text().decode("utf8"))
            #    summary = ""
            #    article = unicode(soup.select("#NewsSummary")[0].get_text().decode("utf8"))
            #    article.replace("SOL"," ")
            #    article.replace("SOLTags"," ")

            #N
            if domain == "www.rtp":
                title = unicode(soup.select("#video_detail")[0].h1.get_text().encode("utf8"))
                summary = ""
                article =  unicode(soup.select("#video_detail")[0].h2.get_text().decode('utf8'))
            
            if title == "":
                return;
            
            if(justDownload == 1):
                return article        
            
            self.storeNew(url,date,domain,title,summary,article);
        except IndexError:
            print "####IndexError: Ignore entry: "+url
            return
        except UnboundLocalError:
            print "####Invalid domain: "+url
            return
        except: 
            print "####Unexpected error: ignore entry:"+url
            return
        
        print "-----", self.Narticles, url, "-----"
        self.Narticles += 1
        #Sacar as entidades e guardar na base de dados das entidades e opinioes
        self.__conn.commit()     
        self.__conn.close()
        result = self.entityExtraction.ParseEntitiesFromDoc(url,title+" "+summary+" "+article)
        self.__conn = sqlite3.connect(self.__dbName)     
        self.__cursor = self.__conn.cursor()  
        self.saveOpinion(result,url)

    
    #Store the article at database and add to whoosh index
    def storeNew(self,url,date,domain,title,summary,article):
        #print "Store content of " + url
        try:
            self.__cursor.execute('Update newsStorage set DOMAIN=?, TITLE=?, SUMMARY=?, ARTICLE=?, DATE=?,PROCESSED="True" where URL=?',(domain,title,summary,article,date,url))
        except sqlite3.IntegrityError:
            pass

        #Adicionar conteudo ao Whoosh Indexer
        self.whoosh.addLink(url, title, summary, article);
    
    #Resultado: {"NomeEntidade", [N_Ocorrencias, Sentimento_Acumulado]}
    def saveOpinion(self,results,url):
        cursorOpinion = self.__conn.cursor()
        cursor = self.__conn.cursor()

        for (entity,value) in results.items():
            cursor.execute('UPDATE personalities SET REPUTATION=(REPUTATION+?) where NAME=?',(value[0],unicode(entity)))
            try:
                cursorOpinion.execute('INSERT into opinion(URL,ENTITY,OPINION) values(?,?,?)',(unicode(url),unicode(entity),value[1]))
            except sqlite3.IntegrityError:
                cursorOpinion.execute('Update opinion set OPINION=? WHERE URL=? and ENTITY=?',(unicode(url),unicode(entity),value[1]))

           
