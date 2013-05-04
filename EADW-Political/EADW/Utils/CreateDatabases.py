'''
Created on May 4, 2013
'''
import os
import sqlite3
from EADW.Utils.ImportFeeds import ImportFeeds
from EADW.Utils.Personalites import ParseFileNames
from EADW.Utils.SentimentsBase import  SentimentParser

#Create news.db
dbpath = "../../storage/news.db"
if not os.path.exists(dbpath):
    print "Create new: "+dbpath
    conn = sqlite3.connect(dbpath)     
    c = conn.cursor()
    c.execute('CREATE TABLE newsStorage (URL text  PRIMARY KEY DEFAULT NULL,DATE date DEFAULT NULL,DOMAIN text DEFAULT NULL,TITLE text DEFAULT NULL,SUMMARY text DEFAULT NULL,ARTICLE text DEFAULT NULL,PROCESSED Boolean DEFAULT FALSE)')
    c.execute('CREATE TABLE opinion (URL TEXT  NOT NULL,ENTITY TEXT  NOT NULL ,OPINION integer,Primary Key(URL,ENTITY))')
    c.execute('''CREATE TABLE personalities (NAME text, NAME_NORM text primary key, PRE_REPUTATION INTEGER, REPUTATION INTEGER,PARTIDO text,GOVERNO text)''')
    conn.commit()
    print "Base de dados Criada"
    
    #Invoke scripts to fullfil Database
    ImportFeeds.GetFeeds(dbpath)


#Create lexicon.db
dbpath = "../../storage/lexicon.db"
if not os.path.exists(dbpath):
    print "Create new: "+dbpath
    conn = sqlite3.connect(dbpath)     
    c = conn.cursor()
    c.execute('''CREATE TABLE properNouns (NOUN text primary key)''')
    c.execute('''CREATE TABLE nameEquiv (NAME text,EQUIV text)''')
    c.execute('''CREATE TABLE rubishNames (RUBISH_NAME text primary key)''')
    c.execute('CREATE TABLE tags (WORD TEXT  NOT NULL,TAG TEXT  NOT NULL ,Primary Key(WORD))')
    ParseFileNames.loadDatabase()
    SentimentParser.Parser(dbpath).DoIt()

print "DONE"