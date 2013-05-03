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
    
    conn2 = sqlite3.connect("../../../news.db")     
    c2 = conn2.cursor()  
    for pair in list:
        #Save at SQL Database
        try:
            c2.execute('Insert into newsStorage(URL,DATE,PROCESSED) values(?,?,"False")',(link,dt))
        except sqlite3.IntegrityError:
            pass
            #already exists
    conn2.commit()
    conn2.close()
    

    
    
GetFeeds()



