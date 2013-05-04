#!/usr/bin/python
# -*- coding: utf-8 -*-
from WooshEngine import WooshEngine

dbpath = "../news.db"

engine = WooshEngine()
engine.setDBName(dbpath);

#search by word:
#Return: link,title,score,summary,global_feeling, 
#entities,global entity reputation,news opinion, partido
def searchNews(search_word):
    result = []
    for score, link, entities in engine.searchTopWithEntity(search_word, 5):
        return "Score: "+str(score), "Link: "+link, "Entities: ", entities



#Entity details
#Nome completo
#Reputacao geral
#N. Noticias positivas
#N. Noticias negativas
#Partido politico
#Nº Positivas por dia
#Nº Negativas por dia
def getEntityDetails(entity):
    return "TODO"

#Lista de partidos:
# -> Numero de noticas
# -> Nº Positivas por dia
# -> Nº Negativas por dia
#Depos faz o acumulado
def partidos():
    return "TODO"

#Quais as palavras mais ditas
def topWords():
    return "TODO"

def topCountries():
    return "TODO"