'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''


from ContentDownloader import ContentDownloader
from threading import Thread
import feedparser
import time
import re
import sqlite3
from time  import mktime
from datetime import datetime

class FeedDownloader(Thread):         
    __feedUrl = ""
    __feed = ""
    __updatePeriod = 60
    __dbName = ""
    __downloader = ""

    def __init__(self, feedUrl,dbName):
        Thread.__init__(self)
        self.__feedUrl = feedUrl
        self.__dbName = dbName
        self.__downloader = ContentDownloader(dbName)
                          
    
    def run(self):
        while(1):
            self.updateList()
            time.sleep(self.__updatePeriod)
            
            
    def updateList(self):
        
        #Download and parse the feed URL
        self.__feed = feedparser.parse(self.__feedUrl)
        
        #Store the Link and Date on Database
        for entry in self.__feed.entries:
            link = entry.link
            date = entry.published_parsed
            dt = datetime.fromtimestamp(mktime(date))
            
            try:
                #Inserir novo link
                conn = sqlite3.connect(self.__dbName)     
                c = conn.cursor()
                c.execute('INSERT INTO newsStorage(URL,DATE) values (?,?)',(link,dt))
                conn.commit()
                print "Date: "+str(dt), "New link: "+link
                
                #Descaregar o conteudo do novo link
                self.__downloader.parseSite(link, dt);
                
            except sqlite3.IntegrityError:
                pass
            
        
                  
