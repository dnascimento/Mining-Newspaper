'''
Created on Mar 25, 2013
'''
from threading import Thread
import urllib
import re
import sqlite3
from bs4 import BeautifulSoup

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database   
class newsParser(Thread):
    
    def __init__(self,dbName):
        Thread.__init__(self)
        self.__domain = domain
        self.__dbName = dbName
      
    
    #Read from DB each entry with: url and Date
    def start(self):
        self.__conn = sqlite3.connect(self.__dbName)     
        cursor = self.__conn.cursor()   
        for row in cursor.execute("Select * from newsStorage where PROCESSED=FALSE"):
                self.parseSite(row[0],row[1])        
        self.printDatabase()
        
    def parseSite(self,url,date,domain):
        fileURL = urllib.urlopen(url)
        
        
        
        doc = fileURL.read()        
        soup = BeautifulSoup(doc)
        try:
            if domain == "expresso.sapo":
                title = soup.select("#artigo")[0].h1.get_text()
                summary = soup.select("#artigo")[0].summary.get_text()
                article =  soup.select("#conteudo")[0].get_text()
                    
            if domain == "feeds.dn":
                title = soup.select("#NewsTitle")[0].get_text()
                summary = soup.select("#NewsSummary")[0].get_text()
                article = soup.select("#Article")[0].get_text()
            
            
            if domain == "rss.feedsportal":
                title = soup.select("#NewsTitle")[0].get_text()
                summary = soup.select("#NewsSummary")[0].get_text()
                article = soup.select("#Article")[0].get_text()
            
            
            if domain == "economico.sapo":
                title = soup.select(".meta")[0].h2.get_text()
                summary = soup.select(".mainText")[0].strong.get_text()
                article = soup.select(".mainText")[0].get_text()
            
            if domain == "www.sol":
                title = soup.select("#NewsTitle")[0].get_text()
                summary = ""
                article = soup.select("#NewsSummary")[0].get_text()
            
            
            if domain == "www.rtp":
                title = soup.select("#video_detail")[0].h1.get_text()
                summary = ""
                article =  soup.select("#video_detail")[0].h2.get_text()
            
            self.storeNew(url,date,domain,title,summary,article);
        except IndexError:
            print "IndexError: Ignore entry: "+url
        except UnboundLocalError:
            print "Invalid domain: "+url
        except: 
            print "Unexpected error: ignore entry:"+url
            
        
            
    def storeNew(self,url,date,domain,title,summary,article):
        print "Add new"
        try:
            cursor = self.__conn.cursor()
            cursor.execute('INSERT INTO newsStorage values (?,?,?,?,?,?)',(url,date,domain,title,summary,article))
        except sqlite3.IntegrityError:
            return
    
    def printDatabase(self):
        cursor = self.__conn.cursor()
        for row in cursor.execute("Select * from newsStorage"):
            print row
        self.__conn.commit()
        



def runParser(dbName):
    #todo corrigir
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    #todo corrgir
    for row in cursor.execute("select distinct(domain) from newsStorage"):
        thread =  newsParser(row[0],dbName)
        thread.start()

#runParser("news.db")

thread =  newsParser("","news.db")
thread.start()
