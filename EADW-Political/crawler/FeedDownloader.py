# -.- coding: utf-8 -.-
from threading import Thread
import feedparser
import time

class FeedDownloader(Thread):
                    
    __feedUrl = ""
    __fileName = ""
    __lastUpdate = ""
    __feed = ""
    __updatePeriod = 2
    __lastDownloaded = set()


    def __init__(self, feedUrl, fileName):
        Thread.__init__(self)
        self.__feedUrl = feedUrl
        self.__fileName = fileName
        self.__feed = feedparser.parse(feedUrl)
        
    
    def run(self):

        while(1):
            self.__checkUpdates()
            time.sleep(self.__updatePeriod)
            
            
    def __checkUpdates(self):
        
        title = self.__feed.entries[0].title
                
        if(not self.__lastUpdate ==  title):
            print "Update Found for feed:", self.__fileName," at ",  title
            self.__lastUpdate = title
            self.__updateList()
    
    
    def __updateList(self):
         
        #a nova lista de links   
        newlinks = set()
        for entry in self.__feed.entries:
            newlinks.add(entry.link)
        
        #os links novos descobertos
        differentLinks = newlinks.difference(self.__lastDownloaded) 
        self.__lastDownloaded = newlinks
        
        #Acrescentar apenas os novos links
        date = self.__feed.updated.split()
        fileDesc = open(self.__fileName+"_"+date[3]+"_"+date[2]+"_"+date[1]+"_"+date[4]+".link" , "w")
        for link in differentLinks:
            fileDesc.write(link + '\n')          

                     
                     
