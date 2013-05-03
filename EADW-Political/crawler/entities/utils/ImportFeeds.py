'''
Created on Mar 25, 2013
'''
import re
from collections import Counter
import sqlite3
import unicodedata
from time  import mktime
from datetime import datetime
import time
import os
#
#Extracts a name:reputation list and a  nomial names list
#
def GetFeeds():
   
    conn = sqlite3.connect("feeds.db")     
    c = conn.cursor()       
    
    list = []
    for pair in c.execute('''select * from feedsCrawling'''):
        link = pair[0]
        date = time.strptime(pair[1],"%Y-%m-%d %H:%M:%S")
        dt = datetime.fromtimestamp(mktime(date))
        a = (link,dt)
        list.append(a)
    
    conn.commit()
    conn.close()
    
    print list
    
    dbpath = "../../../news.db"
    
    if not os.path.exists(dbpath):
        print "Base de dados nao encontrada, Vamos Criar uma Nova"
        conn = sqlite3.connect(dbpath)     
        c = conn.cursor()
        c.execute('CREATE TABLE newsStorage (URL text  PRIMARY KEY DEFAULT NULL,DATE date DEFAULT NULL,DOMAIN text DEFAULT NULL,TITLE text DEFAULT NULL,SUMMARY text DEFAULT NULL,ARTICLE text DEFAULT NULL,PROCESSED Boolean DEFAULT FALSE)')
        c.execute('CREATE TABLE opinion (URL TEXT  NOT NULL,ENTITY TEXT  NOT NULL ,OPINION integer,Primary Key(URL,ENTITY))')
        conn.commit()
        print "Base de dados Criada"
    
    
    conn2 = sqlite3.connect(dbpath)     
    c2 = conn2.cursor()  
    for pair in list:
        #Save at SQL Database
        try:
            c2.execute('Insert into newsStorage(URL,DATE,PROCESSED) values(?,?,"False")',(pair[0],pair[1]))
        except sqlite3.IntegrityError:
            pass
            #already exists
    conn2.commit()
    conn2.close()
    

    
    
GetFeeds()



