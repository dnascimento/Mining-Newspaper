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


#################################################
# Descarregar a lista de feeds do URL que foi passado.
# Ex: Expresso.feeds, vai descarregar todos os links
# para o site do expresso em que estao as novas 
# noticias
###################################################
class FeedDownloader(Thread):         

    def __init__(self, feedUrl,dbName):
        Thread.__init__(self)
        self.__feedUrl = feedUrl
        self.__dbName = dbName
                          
    
    #Thread que vai actualizar a lista de um determinado feed provider (expresso por exemplo)
    def run(self):
            self.updateList()
            
    ################################################################
    #Descarregar a lista de feeds do feed provider, associar a cada
    #um dos feeds a referencia para o site e a data da noticia
    ###############################################################
    def updateList(self):
        print "FeedDownloader: "+self.__feedUrl
        #Download and parse the feed URL
        feed = feedparser.parse(self.__feedUrl)
        
        conn = sqlite3.connect(self.__dbName)     
        cursor = conn.cursor()
          
        #Store the Link and Date on Database
        for entry in feed.entries:
            link = entry.link
            date = entry.published_parsed
            dt = datetime.fromtimestamp(mktime(date))
            
            #Save at SQL Database
            try:
                cursor.execute('Insert into newsStorage(URL,DATE,PROCESSED) values(?,?,"False")',(link,dt))
            except sqlite3.IntegrityError:
                pass
                #already exists
        conn.commit()
        conn.close()
        
    
              
