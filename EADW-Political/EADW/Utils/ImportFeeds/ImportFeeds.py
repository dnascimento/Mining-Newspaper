#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Mar 25, 2013

Importar a lista de URL de feeds que ja existam numa outra base de dados.
Este script permite importar a lista gerada por outro servidor que temos a 
correr 24 horas por dia e que vai adquirindo os URL
'''
import re
from collections import Counter
import sqlite3
import unicodedata
from time  import mktime
from datetime import datetime
import time
import os
##################################################################
#Extracts a name:reputation list and a  nomial names list
##################################################################
def GetFeeds(dbpath):
   
    conn = sqlite3.connect("ImportFeeds/feeds.db")     
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
    
    #print list
        
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
    



