from FeedDownloader import FeedDownloader
from WooshEngine import WooshEngine
from TAGAnalizer import TAGAnalizer
from ContentDownloader import ContentDownloader
import os
import sqlite3

#
#Inicializa o Woosh e a database
#Descarregar os links de cada um dos sites de feeds
#
dbpath = "../news.db"


##Criar base de dados se nao exestir
if not os.path.exists(dbpath):
    print "Base de dados nao encontrada, Vamos Criar uma Nova"
    conn = sqlite3.connect(dbpath)     
    c = conn.cursor()
    c.execute('CREATE TABLE newsStorage (URL text  PRIMARY KEY DEFAULT NULL,DATE date DEFAULT NULL,DOMAIN text DEFAULT NULL,TITLE text DEFAULT NULL,SUMMARY text DEFAULT NULL,ARTICLE text DEFAULT NULL,PROCESSED Boolean DEFAULT FALSE)')
    c.execute('CREATE TABLE opinion (URL TEXT  NOT NULL,ENTITY TEXT  NOT NULL ,OPINION integer,Primary Key(URL,ENTITY))')
    conn.commit()
    conn.close()
    print "Base de dados Criada"

##Criar a base de dados de pesquisa de TAGS
tag = TAGAnalizer()
tag.loadToDB()


##Criar motor de Pesquisa Baseado no Woosh se nao existir
print "Adicionar Conteudo ao Woosh Indexer"
engine = WooshEngine()
engine.setDBName(dbpath);
engine.createIndex()


#TODO Tornar async

#Descarregar todas as feeds
dn = FeedDownloader("http://feeds.dn.pt/DN-Politica",dbpath)
dn.updateList()

jn = FeedDownloader("http://feeds.jn.pt/JN-Politica",dbpath)
jn.updateList()

vg = FeedDownloader("http://economico.sapo.pt/rss/politica",dbpath)
vg.updateList()

sol = FeedDownloader("http://sol.sapo.pt/rss/",dbpath)
sol.updateList()


#Esperar que as threads de download dos  links terminem

#Processar as feeds pendents 
#Adicionar e Descarregar o conteudo dos novos links e processar todos
downloader = ContentDownloader(dbpath)
downloader.start();        
 

