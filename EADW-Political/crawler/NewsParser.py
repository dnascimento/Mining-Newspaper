'''
Created on Mar 25, 2013

@author: darionascimento
'''

import urllib
import re
import sqlite3
from bs4 import BeautifulSoup

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database
class newsParser:
    
    #Read from DB each entry with: url and Date
    def readFromDB(self,dbName):
        self.__dbName = dbName
        conn = sqlite3.connect(dbName)
        self.__cursor = conn.cursor()
        try:
            self.__cursor.execute('''CREATE TABLE newsStorage  (url text,date date,domain text,title text,summary text, article text, UNIQUE(url))''')
        except sqlite3.OperationalError:
            pass 
        
        for row in self.__cursor.execute("Select * from feedsCrawling"):
            self.parseSite(row[0],row[1])
           
        
    def parseSite(self,url,date):
        fileURL = urllib.urlopen(url)
        
        domain = re.split("http://",url)[1]        
        domain = re.split("\.pt|\.com",domain)[0]
        
        doc = fileURL.read()        
        soup = BeautifulSoup(doc)
                
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
            title = soup.select(".meta")[0].h2.get_text().decode("utf-8")
            summary = soup.select(".mainText")[0].strong.get_text().decode("utf-8")
            article = soup.select(".mainText")[0].get_text().decode("utf-8")
        
        if domain == "www.sol":
            title = soup.select("#NewsTitle")[0].get_text()
            summary = ""
            article = soup.select("#NewsSummary")[0].get_text()
        
        
        if domain == "www.rtp":
            title = soup.select("#video_detail")[0].h1.get_text()
            summary = ""
            article =  soup.select("#video_detail")[0].h2.get_text()
        
        self.storeNew(url,date,domain,title,summary,article);
        
    def storeNew(self,url,date,domain,title,summary,article):
        print "Add new"
        try:
            self.__cursor.execute('INSERT INTO newsStorage values (?,?,?,?,?,?)',(url,date,domain,title,summary,article))
        except sqlite3.IntegrityError:
            pass
    
    def printDatabase(self):
        for row in self.__cursor.execute("Select * from newsStorage"):
            print row

    
parser  = newsParser()
parser.readFromDB("feeds.db")
parser.printDatabase()