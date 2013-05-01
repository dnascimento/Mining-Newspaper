'''
Created on Mar 25, 2013
'''
from threading import Thread
from bs4 import BeautifulSoup
from sqlite3 import OperationalError
from WooshEngine import WooshEngine

import urllib
import re
import sqlite3
import EntityExtraction
from bs4 import BeautifulSoup

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database   
class ContentDownloader(Thread):
    
    __dbName = ""
    whoosh = ""
    
    def __init__(self,dbName):
        Thread.__init__(self)
        self.__dbName = dbName
	self.entityExtraction = entities.EntityExtract.EntityExtractor()
 	self.whoosh = WooshEngine()
      
    
    #Old
    #Read from DB each entry with: url and Date
    def start(self):
        self.__conn = sqlite3.connect(self.__dbName)     
        cursor = self.__conn.cursor()   
        for row in cursor.execute("Select * from newsStorage where PROCESSED=0"):
                self.parseSite(row[0],row[1])        
        #self.printDatabase()
        
    def parseSite(self,url,date):
        fileURL = urllib.urlopen(url)
        
        domain = re.split("http://",url)[1]        
        domain = re.split("\.pt|\.com",domain)[0]
            
        doc = fileURL.read()        
        soup = BeautifulSoup(doc)
        try:
            if domain == "expresso.sapo":
                title = unicode(soup.select("#artigo")[0].h1.get_text())
                summary = unicode(soup.select("#artigo")[0].summary.get_text())
                article =  unicode(soup.select("#conteudo")[0].get_text())
                    
            if domain == "feeds.dn":
                title = unicode(soup.select("#NewsTitle")[0].get_text())
                summary = unicode(soup.select("#NewsSummary")[0].get_text())
                article = unicode(soup.select("#Article")[0].get_text())
            
            
            if domain == "rss.feedsportal":
                title = unicode(soup.select("#NewsTitle")[0].get_text())
                summary = unicode(soup.select("#NewsSummary")[0].get_text())
                article = unicode(soup.select("#Article")[0].get_text())
            
            
            if domain == "economico.sapo":
                title = unicode(soup.select(".meta")[0].h2.get_text())
                summary = unicode(soup.select(".mainText")[0].strong.get_text())
                article = unicode(soup.select(".mainText")[0].get_text())
            
            if domain == "www.sol":
                title = unicode(soup.select("#NewsTitle")[0].get_text())
                summary = ""
                article = unicode(soup.select("#NewsSummary")[0].get_text())
                article.replace("SOL"," ")
                article.replace("SOLTags"," ")

            
            if domain == "www.rtp":
                title = unicode(soup.select("#video_detail")[0].h1.get_text())
                summary = ""
                article =  unicode(soup.select("#video_detail")[0].h2.get_text().decode('utf8'))
            
            self.storeNew(url,date,domain,title,summary,article);
        except IndexError:
            print "####IndexError: Ignore entry: "+url
        except UnboundLocalError:
            print "####Invalid domain: "+url
        except OperationalError:
            print "####Base de dados Fechada, (MultiTHread) tentando outra vez"
            self.storeNew(url,date,domain,title,summary,article);
            
        #except: 
        #    print "####Unexpected error: ignore entry:"+url
        
        #TODO send to whosh: Name tag etc
        print url
        result = self.entityExtraction.ParseEntitiesFromDoc(title+" "+summary+" "+article)
        self.storeResult(url,result)
        
    
    def storeResult(self,url,result):
        cursor = self.__conn.cursor()
        for (entity,counter) in result.items():
            try:
                cursor.execute('INSERT into opinion values(?,?,?)',(unicode(url),unicode(entity),counter))
            except sqlite3.IntegrityError:
                cursor.execute('Update opinion set OPINION=? WHERE URL=? and ENTITY=?',(unicode(url),unicode(entity),counter))
        self.__conn.commit()
        
    def storeNew(self,url,date,domain,title,summary,article):
        print "    Updating Content Info for " + url
        conn = sqlite3.connect(self.__dbName)     
        cursor = conn.cursor()
        cursor.execute('UPDATE newsStorage set DOMAIN=?, TITLE=?, SUMMARY=?, ARTICLE=? where url=?',(domain,title,summary,article,url))
        conn.commit()
        
        #print "----->"
        #print url, unicode(title), unicode(summary), unicode(article)
        #print "<-----"
        #Adicionar conteudo ao Whoosh Indexer
        #print "---Woosh IN---"
        self.whoosh.addLink(url, title, summary, article);
        #print "---Woosh IN---"

#ContentDownloader("news.db").start()
#   def printDatabase(self):
#      cursor = self.__conn.cursor()
#     for row in cursor.execute("Select * from newsStorage"):
#        print row
    #    self.__conn.commit()
