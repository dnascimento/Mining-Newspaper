#!/usr/bin/python
# -*- coding: utf-8 -*-

#import nltk
import nltk
from nltk.corpus import floresta
from pprint import pprint
import  entities.WordProcessor as WordProcessor
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
    
    __dBEntitiesLocation = "../entities.db"
    lixo  = nltk.corpus.stopwords.words('portuguese')
    opinionAnalist = Opinion()

    def __init__(self):
        self.ProperNameProcessor = WordProcessor.ProperNameProcessor()
        conn = sqlite3.connect(self.__dBEntitiesLocation)
        cursor = conn.cursor()
        self.rubishProperNounList = []
        for row in cursor.execute("Select * from rubishNames"):
            self.rubishProperNounList.append(row[0]) 
        conn.close()
        
        #self.LoadTagTree()
        
       
        
        
        
    def ParseEntitiesFromDoc(self,url,doc):
        
        self.ProperNameProcessor.init()
        results = dict()
        sentences = nltk.sent_tokenize(doc.decode("utf8"))
                    
        for sentence in sentences:
            
            self.ProperNameProcessor.init()
            
            # Remove POntuacoo
            # nao pode ser pelo ntlk senao faz parse as palavras
            for c in string.punctuation:
                sentence = sentence.replace(c,"")

            words = sentence.split(" ")
            tagger = TAGAnalizer()
            
            for word in words:
    
                #retira lixo
                if(len(word) < 2):
                    continue
                
                # verifica se pretence a lista de stop words
                if(word.lower() in self.lixo):
                    continue
                
                POS = tagger.getTagFromBD(word)
            
                if  POS == 'NPROP': 
                    
                    #its properNoun
                    self.ProperNameProcessor.updateNewName(word,True) 
                else:
                    self.ProperNameProcessor.updateNewName(word,False) 
            
            #contar o numero de ocorrencias
            #associar o feeling da frase a esta entidade
            entities = self.ProperNameProcessor.doFinal()
            counting = Counter(entities.values())
            
            
            feeling = self.getFeelingAndAdjectives(sentence)[0]
            adjectives = self.getFeelingAndAdjectives(sentence)[1]
            # TODO Dario Usar os Ajectivos
            
            # Somar ocorrencias e sentimento da frase
            for (entity,appears) in counting.items():
                if entity not in results:
                    results[entity] = [appears,feeling]
                    print entity, feeling
                else:
                    results[entity][0] += appears
                    results[entity][1] += feeling
            
        #Store results
        #print results
        return results
        #TODO Check wich entities are recognized officialy
   
   
    def getFeelingAndAdjectives(self,sentence):
        return self.opinionAnalist.getSentenceOpinion(sentence)
        
    #This doesnt noun belongs to "blacklist" and it start with capital letter
    def itsNotRubisProperNoun(self,noun):
        if(re.match('[A-Z]',noun) == None):
            return False
        
        noun = noun.lower()
        return len(set([noun]).difference(self.rubishProperNounList)) != 0
    
        
    
    
    
    
    
    
    
    


