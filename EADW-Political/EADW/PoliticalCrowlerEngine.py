#!/usr/bin/env python
# -*- coding: utf-8 -*-
from EADW.Analisers.WooshEngine import WooshEngine
from EADW.Downloaders.FeedDownloader import FeedDownloader
from  EADW.Downloaders.ContentDownloader import ContentDownloader
import os 
import sqlite3

dbpath = "../storage/news.db"


def justRecentNews():
    conn = sqlite3.connect(dbpath)     
    cursor = conn.cursor()   
    cursor.execute("DELETE from opinion")
    cursor.execute("DELETE from newsStorage")
    conn.commit()
    conn.close()
#
#Inicializa o Woosh e a database
#Descarregar os links de cada um dos sites de feeds
#

##Criar base de dados se nao exestir
if not os.path.exists(dbpath):
    print "Base de dados nao encontrada. Inicie o sistema pelo Utils, CreateDatabases em EADW.Utils.CreateDatabases"
else:
    #justRecentNews()
    
    
    ##Criar motor de Pesquisa Baseado no Woosh se nao existir
    print "Adicionar Conteudo ao Woosh Indexer"
    engine = WooshEngine()
    engine.setDBName(dbpath);
    engine.createIndex()
    
    
    
    #Descarregar todas as feeds
    #.decode('ISO 8859-1')
    dn = FeedDownloader("http://feeds.dn.pt/DN-Politica",dbpath)
    dn.updateList()
    
    jn = FeedDownloader("http://feeds.jn.pt/JN-Politica",dbpath)
    jn.updateList()
    
    
    vg = FeedDownloader("http://economico.sapo.pt/rss/politica",dbpath)
    vg.updateList()
    
    
    sol = FeedDownloader("http://sol.sapo.pt/rss/",dbpath)
    sol.updateList()
    
    
    #Processar as feeds pendents 
    #Adicionar e Descarregar o conteudo dos novos links e processar todos
    downloader = ContentDownloader(dbpath)
    downloader.start();        
     
    
