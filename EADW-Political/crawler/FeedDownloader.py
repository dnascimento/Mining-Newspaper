'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''



from threading import Thread
import feedparser
import time
import sqlite3
from time  import mktime
from datetime import datetime

class FeedDownloader(Thread):
                    
    __feedUrl = ""
    __feed = ""
    __updatePeriod = 5
    __dbName = ""


    def __init__(self, feedUrl,dbName):
        Thread.__init__(self)
        self.__feedUrl = feedUrl
        self.__dbName = dbName
      
                    
    
    def run(self):
        while(1):
            self.updateList()
            time.sleep(self.__updatePeriod)
            
            
    
      
    
    
    def updateList(self):
           #Load SQLite DB
        try:
           conn = sqlite3.connect( self.__dbName)
           c = conn.cursor()
           c.execute('''CREATE TABLE feedsCrawling  (url text,date date, UNIQUE(url))''')
        except sqlite3.OperationalError:
           pass
            
            
        self.__feed = feedparser.parse(self.__feedUrl)

        for entry in self.__feed.entries:
            link = entry.link
            date = entry.published_parsed
            dt = datetime.fromtimestamp(mktime(date))

            try:
                c.execute('INSERT INTO feedsCrawling values (?,?)',(link,dt))
                print "New link: "+link
            except sqlite3.IntegrityError:
                pass
            
            
        conn.commit()
         
       # for row in c.execute("Select * from feedsCrawling"):
        #    print row
        

                     
                     
