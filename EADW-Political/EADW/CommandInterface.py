#!/usr/bin/python
# -*- coding: utf-8 -*-
from EADW.Analisers.WooshEngine import WooshEngine
import sqlite3
import unicodedata
import time
import datetime

dbpath = "../storage/news.db"

engine = WooshEngine()
engine.setDBName(dbpath);

#search by word:
#Return: link,title,score,summary,global_feeling, 
#entities,global entity reputation,news opinion
def searchNews(search_word):
    #ir ao woosh buscar 
    news = engine.searchTopWithEntity(search_word,10)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    results = []
    
    for new in news:
        #score|url|[entities]
        score = new[0]
        url = new[1]
        #entidades da noticia e respectiva opiniao
        entities = c.execute("select ENTITY,OPINION from opinion where URL=?",[url])
        globalFeeling = 0
        entitiesList = []
        for entity in entities:
            globalFeeling += entity[1]
            print entity[0]
            try:
                name = entity[0].decode('utf-8')
            except UnicodeDecodeError:
                name = entity[0]  
            entitiesList.append([name,entity[1]])
            
        cont = c.execute("select URL,TITLE,SUMMARY,ARTICLE from newsStorage where URL=?",[url])
        newContent = cont.fetchone()
        
        summary = newContent[2]
        if summary:
            summary[:100]
        else:
            summary = newContent[3][:100]
    
        try:
            title = newContent[1].decode('utf-8')
        except UnicodeDecodeError:
            title = newContent[1]
        
        try:
            summary = summary.decode('utf-8')
        except UnicodeDecodeError:
            summary = summary.encode('utf-8')
        
        summary +="..."
        result = {"link":newContent[0],"title":title,"score":score,"summary":summary,
                "globalFeeling":globalFeeling,"entities":entitiesList}
        
        results.append(result)
    return results


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
    entity = unicode(entity)
    name_norm = unicode(unicodedata.normalize('NFKD', unicode(entity).lower()).encode('ASCII', 'ignore'))
    details = c.execute("select NAME,NAME_NORM,PRE_REPUTATION,REPUTATION,PARTIDO,GOVERNO from personalities where NAME_NORM=?",[name_norm])
    details = details.fetchone()
    if not details:
        return None
    
    name = details[0]
    partido = details[4]
    governo = details[5]
    reputacao = details[3]
    
    noticiasPositivasPorDia = genGraphData(c.execute("select count (*),DATE from opinion natural join newsStorage where OPINION > 0 and ENTITY=? GROUP BY strftime('%Y-%m-%d', DATE)",[name]))
    noticiasNeutrasPorDia = genGraphData(c.execute("select count (*),DATE from opinion natural join newsStorage where OPINION == 0 and ENTITY=? GROUP BY strftime('%Y-%m-%d', DATE)",[name]))
    noticiasNegativasPorDia = genGraphData(c.execute("select count (*),DATE from opinion natural join newsStorage where OPINION < 0 and ENTITY=? GROUP BY strftime('%Y-%m-%d', DATE)",[name]))
    opinion = genGraphData(c.execute("select sum(OPINION), DATE from opinion natural join newsStorage where  ENTITY=? GROUP BY strftime('%Y-%m-%d', DATE)",[name]))

    adjs = c.execute("select ADJECTIVE,COUNT from entityAdjectives where ENTITY_NORM=? order by COUNT DESC LIMIT 20",[name_norm])
    adjectives = []
    i = 0
    for adjective in adjs:
        
        adjectives.append(adjective)


    if partido:
        partido = partido.decode('utf-8')
    if governo:
        governo = governo.decode('utf-8')
    
    data = [{"key":"Positive News", "values":noticiasPositivasPorDia},
           {"key":"Neutral News", "values":noticiasNeutrasPorDia},
           {"key":"Negative News", "values":noticiasNegativasPorDia},
           {"key":"Opinion", "values":opinion}]
    return {"entity":name.decode('utf-8'),"reputation":reputacao,"data":data, 
            "partido":partido,"governo":governo,"adjectives":adjectives}


#Lista de partidos:
# -> Numero de noticas
# -> Nº Positivas por dia
# -> Nº Negativas por dia
#Depos faz o acumulado
def partidosPositive():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    partidos = c.execute("select distinct PARTIDO from personalities where PARTIDO != ''")
    result = []
    parts = []
    for partido in partidos:
        parts.append(str(partido[0]))
        
    for partido in parts:
        partido = unicode(partido)
        noticiasPositivasPorDia = genGraphData(c.execute("select count (URL),DATE  from opinion natural join newsStorage natural join personalities where OPINION > 0 and PARTIDO=? GROUP BY strftime('%Y-%m-%d', DATE)",[partido]))
        result.append({"key":partido, "values":noticiasPositivasPorDia})  
    
    print result
    return  {"data":result}

def partidosNeutral():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    partidos = c.execute("select distinct PARTIDO from personalities where PARTIDO != ''")
    result = []
    parts = []
    for partido in partidos:
        parts.append(str(partido[0]))
        
    for partido in parts:
        partido = str(partido)
        noticiasNeutrasPorDia = genGraphData(c.execute("select count (URL),DATE from opinion natural join newsStorage natural join personalities where OPINION == 0 and PARTIDO=? GROUP BY strftime('%Y-%m-%d', DATE)",[partido]))
        result.append({"key":partido, "values":noticiasNeutrasPorDia})        
    return  {"data":result}


def partidosNegative():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    partidos = c.execute("select distinct PARTIDO from personalities where PARTIDO != ''")
    result = []
    parts = []
    for partido in partidos:
        parts.append(str(partido[0]))
    for partido in parts:
        partido = str(partido)
        print partido    
        noticiasNegativasPorDia = genGraphData(c.execute("select count (URL),DATE from opinion natural join newsStorage natural join personalities where OPINION < 0 and PARTIDO=? GROUP BY strftime('%Y-%m-%d', DATE)",[partido]))
        result.append({"key":partido, "values":noticiasNegativasPorDia})
        
    return  {"data":result}

    
    
def partidosOpinion():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    partidos = c.execute("select distinct PARTIDO from personalities where PARTIDO != ''")
    result = []
    parts = []
    for partido in partidos:
        parts.append(str(partido[0]))
    for partido in parts:
        partido = str(partido)
        print partido    
        opinion = genGraphData(c.execute("select sum(OPINION), DATE from opinion natural join newsStorage natural join personalities where  PARTIDO=? GROUP BY strftime('%Y-%m-%d', DATE)",[partido]))
        result.append({"key":partido, "values":opinion})    
    return  {"data":result}
    

#Quais as palavras mais ditas
def topWords():
    return engine.getMostFrequentWords()

def topCountries():
    return engine.getMostFrequentCountries()


def genGraphData(sqlObject):
    #numNoticias,Data,opinionTotal
    result = []
    for day in sqlObject:
        date = dateToTimestamp(day[1])
        result.append([date,day[0]])
    return result
    
def dateToTimestamp(date):
    date = date.split(" ")[0]
    tempo = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
    return int(tempo * 1000)

