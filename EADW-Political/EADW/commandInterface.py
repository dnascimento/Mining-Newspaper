#!/usr/bin/python
# -*- coding: utf-8 -*-
from EADW.Analisers.WooshEngine import WooshEngine
import sqlite3

dbpath = "../storage/news.db"

engine = WooshEngine()
engine.setDBName(dbpath);

#search by word:
#Return: link,title,score,summary,global_feeling, 
#entities,global entity reputation,news opinion, partido
def searchNews(search_word):
    #ir ao woosh buscar 
    result = engine.searchTopWithEntity(search_word,10)
    entities = []
    
    getEntityBasicDetails(name)
    
    entities.append({"entityName":"Dario","entityGlobalReputation":"32","opinion":"1","partido":"PSD"})    
    
    return {"link":"http://www.ist.utl.pt","title":"Dario IST","score":"12","summary":"Summary do texto",
                "globalFeeling":"dario","entities":entities}
    #for score, link, entities,summary,title in engine.searchTopWithEntity(search_word, 5):
        #for entity in entitiesList:
        #return "Score: "+str(score), "Link: "+link, "Entities: ", entities


#Nome, reputacao, partido, governo
def getEntityBasicDetails(name):
    conn = sqlite3.connect(dbpath)
    n = conn.cursor()
    

#Entity details
#Nome completo
#Reputacao geral
#N. Noticias positivas
#N. Noticias negativas
#Partido politico
#Nº Positivas por dia
#Nº Negativas por dia
def getEntityDetails(entity):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    
    entityBasicDetails = c.execute("select NAME,NAME_NORM,PRE_REPUTATION,REPUTATION,PARTIDO,GOVERNO from personalities where NAME_NORME")
    
    pos = {"432434":"12","432434":"12","432434":"12","432434":"12","432434":"12","432434":"12"}
    neg = {"432434":"12","432434":"12","432434":"12","432434":"12","432434":"12","432434":"12"}
    return {"entity":"Dario","reputation":"123","pos":13,"neg":15,"partido":"PSD","pos":pos,"neg":neg}




#Lista de partidos:
# -> Numero de noticas
# -> Nº Positivas por dia
# -> Nº Negativas por dia
#Depos faz o acumulado
def partidos():
    pos = {"432434":"12","432434":"12","432434":"12","432434":"12","432434":"12","432434":"12"}
    neg = {"432434":"12","432434":"12","432434":"12","432434":"12","432434":"12","432434":"12"}
    return {"nNoticias":132,"pos":pos,"neg":neg}

#Quais as palavras mais ditas
def topWords():
    return {"dario":43,"dara":32,"daasd":12,"dadasda":65,"addadsada":323}

def topCountries():
    return {"portugal":43,"espanha":32,"turquia":12,"italia":65,"bulgaria":323}



print searchNews("coelho")