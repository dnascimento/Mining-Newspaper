'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''



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

    def __init__(self, feedUrl,dbName):
        Thread.__init__(self)
        self.__feedUrl = feedUrl
        self.__dbName = dbName
                          
    
    def run(self):
        while(1):
            self.updateList()
            #TODO invoke ContentDownloader
            time.sleep(self.__updatePeriod)
            
            
    def updateList(self):       
       #Download and parse the feed URL
        self.__feed = feedparser.parse(self.__feedUrl)
        
        conn = sqlite3.connect(self.__dbName)     
        c = conn.cursor()

        #Store the Link and Date on Database
        for entry in self.__feed.entries:
            link = entry.link
            date = entry.published_parsed
            dt = datetime.fromtimestamp(mktime(date))
            
            try:
                c.execute('INSERT INTO newsStorage(URL,DATE) values (?,?)',(link,dt))
                print "New link: "+link
            except sqlite3.IntegrityError:
                pass
            
        conn.commit()
         
         
print "NewsCrawler V8"
dn = FeedDownloader("http://feeds.dn.pt/DN-Politica","news.db")
dn.start()

jn = FeedDownloader("http://feeds.jn.pt/JN-Politica","news.db")
jn.start()

vg = FeedDownloader("http://economico.sapo.pt/rss/politica","news.db")
vg.start()

sol = FeedDownloader("http://sol.sapo.pt/rss/","news.db")
sol.start()
                  
