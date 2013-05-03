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
import entities.EntityExtract

#News Parser:
#Download the news from newsletter website and parse them. Retrieves database and parse it to a new database   
class ContentDownloader(Thread):
    
    __dbName = ""
    whoosh = ""
    __dBEntitiesLocation = "../entities.db"
    
    def __init__(self,dbName):
        Thread.__init__(self)
        self.__dbName = dbName
        self.entityExtraction = entities.EntityExtract.EntityExtractor()
        self.whoosh = WooshEngine()
    
    #Read from DB each entry with: url and Date
    def start(self):
        self.__conn = sqlite3.connect(self.__dbName)     
        self.__cursor = self.__conn.cursor()   
        print "Download Content Start"
        #Take a pendent processing elements snapshot
        i = 0
        for row in self.__cursor.execute("Select * from newsStorage where PROCESSED='False'"):
            self.parseSite(row[0],row[1])
            i +=1
            if(i > 10):
                self.__conn .commit()
                i = 0 #part commit
                
        self.__conn .commit()
        self.__conn .close()      
     
        

    ######################################################
    #####  Download site content and store it on database
    ######################################################
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
            
            if title == "":
                return;
            
            self.storeNew(url,date,domain,title,summary,article);
            
        except IndexError:
            print "####IndexError: Ignore entry: "+url
            return
        except UnboundLocalError:
            print "####Invalid domain: "+url
            return
        #except OperationalError:
        #   print "####Base de dados Fechada, (MultiTHread) tentando outra vez"
        #  self.storeNew(url,date,domain,title,summary,article);
        #except: 
            #print "####Unexpected error: ignore entry:"+url
        
        print url
        #Sacar as entidades e guardar na base de dados das entidades e opinioes
        #TODO lancar assync
        result = self.entityExtraction.ParseEntitiesFromDoc(url,title+" "+summary+" "+article)
        self.saveOpinion(result,url)

    
    #Store the article at database and add to whoosh index
    def storeNew(self,url,date,domain,title,summary,article):
        print "Store content of " + url
        cursor = self.__conn.cursor()
        try:
            cursor.execute('Update newsStorage set DOMAIN=?, TITLE=?, SUMMARY=?, ARTICLE=?, DATE=?,PROCESSED="True" where URL=?',(domain,title,summary,article,date,url))
        except sqlite3.IntegrityError:
            pass
        #except OperationalError:
        #   self.storeNew(url,date,domain,title,summary,article)

        #print url, unicode(title), unicode(summary), unicode(article)
        #Adicionar conteudo ao Whoosh Indexer
        #TODO lancar assync
        self.whoosh.addLink(url, title, summary, article);
    
    #Resultado: {"NomeEntidade", [N_Ocorrencias, Sentimento_Acumulado]}
    def saveOpinion(self,results,url):
        connEntities = sqlite3.connect(self.__dBEntitiesLocation)
        cursorEntities = connEntities.cursor()
        cursorOpinion = self.__conn.cursor()
        
        for (entity,value) in results.items():
            cursorEntities.execute('UPDATE personalities SET REPUTATION=(REPUTATION+?) where NAME=?',(value[0],unicode(entity)))
            try:
                cursorOpinion.execute('INSERT into opinion(URL,ENTITY,OPINION) values(?,?,?)',(unicode(url),unicode(entity),value[1]))
            except sqlite3.IntegrityError:
                cursorOpinion.execute('Update opinion set OPINION=? WHERE URL=? and ENTITY=?',(unicode(url),unicode(entity),value[1]))
        connEntities.commit()
        connEntities.close()
           
