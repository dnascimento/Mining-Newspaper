from FeedDownloader import FeedDownloader
from WooshEngine import WooshEngine
import os
import sqlite3


#dbpath = "../Temp.db"
dbpath = "../news.db"


##Criar base de dados se nao exestir
if not os.path.exists(dbpath):
    print "Base de dados nao encontrada, Vamos Criar uma Nova"
    conn = sqlite3.connect(dbpath)     
    c = conn.cursor()
    c.execute('CREATE TABLE newsStorage (URL text  PRIMARY KEY DEFAULT NULL,DATE date DEFAULT NULL,DOMAIN text DEFAULT NULL,TITLE text DEFAULT NULL,SUMMARY text DEFAULT NULL,ARTICLE text DEFAULT NULL,PROCESSED Boolean DEFAULT FALSE)')
    c.execute('CREATE TABLE opinion (URL TEXT  NOT NULL,ENTITY TEXT  NOT NULL ,OPINION integer,Primary Key(URL,ENTITY))')
    conn.commit()
    print "Base de dados Criada"


##Criar motor de Pesquisa Baseado no Woosh se nao existir
print "Adicionar Conteudo ao Woosh Indexer"
engine = WooshEngine()
engine.createIndexDirIfNotExist()
engine.setDBName(dbpath);
engine.createIndex()



dn = FeedDownloader("http://feeds.dn.pt/DN-Politica",dbpath)
dn.start()

jn = FeedDownloader("http://feeds.jn.pt/JN-Politica",dbpath)
jn.start()

vg = FeedDownloader("http://economico.sapo.pt/rss/politica",dbpath)
vg.start()

sol = FeedDownloader("http://sol.sapo.pt/rss/",dbpath)
sol.start()

