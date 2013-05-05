#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import floresta
from pprint import pprint
from  EADW.Analisers import WordProcessor
import sqlite3
import re
import unicodedata
import string
from collections import Counter
from TAGAnalizer import TAGAnalizer
from OpinionAnalysis import Opinion
#Ler cada um dos textos nao processados
#Realizar a analise com o NLTK


class EntityExtractor:
    __pathToNews = "../storage/news.db"
    __dBLexiconLocation = "../storage/lexicon.db"
    lixo  = nltk.corpus.stopwords.words('portuguese')
    opinionAnalist = Opinion()
    tagger = TAGAnalizer()
    IgnoreFile = "Utils/SentimentsBase/in/IgnoreNamesTrainingSet.txt"

    ########################################################
    #Load rubish names list and init properNameProcessor
    #########################################################
    def __init__(self):
        self.ProperNameProcessor = WordProcessor.ProperNameProcessor()
        self.LoadIgnoreList(self.IgnoreFile)#Adiciona a lista "lixo" palavras geradas pelo traning set
        #conn = sqlite3.connect(self.__dBLexiconLocation)
        #cursor = conn.cursor()
        #self.rubishProperNounList = []
        #for row in cursor.execute("Select * from rubishNames"):
        #    self.rubishProperNounList.append(row[0]) 
        #conn.close()
        
    def LoadIgnoreList(self,IgnoreFilePath):
        fd = open(IgnoreFilePath, "r")
        list = fd.read().split(":")
        print "Loaded ignore list\n"
        self.lixo += list
    
    def strip_punctuation(self,text):
        punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
        return ''.join(x for x in text if unicodedata.category(x) not in punctutation_cats)
    
    ########################################################
    #Parse the doc, get entities, analysis etc
    ########################################################
    def ParseEntitiesFromDoc(self,url,doc):
        
        self.ProperNameProcessor.init()
        results = dict()
        sentences = nltk.sent_tokenize(doc.decode("utf8"))
                    
        for sentence in sentences:
            sentence = self.strip_punctuation(sentence)
            words = sentence.split(" ")
            for word in words:
                #retira lixo
                if(len(word) < 2):
                    continue
                
                # verifica se pretence a lista de stop words
                if(word in self.lixo):
                    continue
                
                POS = self.tagger.getTagFromBD(word)
            
            
                #se for nome proprio e comecar por letra maiuscula
                if  (POS == 'NPROP') and self.checkFormat(word): 
                    #its properNoun
                    self.ProperNameProcessor.updateNewName(word,True) 
                else:
                    self.ProperNameProcessor.updateNewName(word,False) 
            
            #contar o numero de ocorrencias
            #associar o feeling da frase a esta entidade
            entities = self.ProperNameProcessor.doFinal()
            counting = Counter(entities.values())
            
            feelingAndAbjectives = self.opinionAnalist.getSentenceOpinion(sentence)
            feeling = feelingAndAbjectives[0]
            adjectives = feelingAndAbjectives[1]
            self.saveAdjectives(entities,adjectives)
            # TODO Dario Usar os Ajectivos
            
            
            # Somar o numero de ocorrencias do nome
            # e a opiniao acumulada sobre o nome
            for (entity,appears) in counting.items():
                if entity not in results:
                    results[entity] = [appears,feeling]
                    print entity, feeling
                else:
                    results[entity][0] += appears
                    results[entity][1] += feeling
            
        return results
   
   
   
    def saveAdjectives(self,entities,adjectives):
        conn = sqlite3.connect(self.__pathToNews)
        cursor = conn.cursor()
        #para cada entidade, adicionar cada adjectivo
        for entity in entities:
            entity = unicode(unicodedata.normalize('NFKD', unicode(entity).lower()).encode('ASCII', 'ignore'))
            for adjective in adjectives:
                try:
                    cursor.execute('INSERT INTO entityAdjectives(ADJECTIVE,ENTITY_NORM,COUNT) values (?,?,?)',[unicode(adjective),entity,1])
                except sqlite3.IntegrityError:
                    cursor.execute('UPDATE entityAdjectives SET COUNT=(COUNT+1) where ADJECTIVE=? and ENTITY_NORM=?',[unicode(adjective),entity])
                                   
        conn.commit()
        conn.close()
    
    #Um nome comeca sempre por uma letra maiuscula
    def checkFormat(self,word):
        return word[0].isupper()
    
    
    
    
    


