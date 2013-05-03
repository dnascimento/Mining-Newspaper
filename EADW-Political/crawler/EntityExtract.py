'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''

#import nltk
import nltk
from nltk.corpus import floresta
from pprint import pprint
import  entities.WordProcessor as WordProcessor
import sqlite3
import re
import unicodedata
from collections import Counter
from TAGAnalizer import TAGAnalizer
#Ler cada um dos textos nao processados
#Realizar a analise com o NLTK


class EntityExtractor:
    __dBEntitiesLocation = "../entities.db"
    
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
        #split the doc in sentences
        #sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        
        #Resultado: {"NomeEntidade", [N_Ocorrencias, Sentimento_Acumulado]}
        results = dict()
        #sentences = nltk.sent_tokenize(doc)
        #tagger = nltk.data.load(nltk.tag._POS_TAGGER)
        
        #print "---->"
        print str(doc)
        #print "<---->"
        doc = unicode(unicodedata.normalize('NFKD', unicode(doc).lower()).encode('ASCII', 'ignore'))
        print doc 
        #print "<----"
        
        sentences = nltk.sent_tokenize(doc)
        for sentence in sentences:
            #print sentence
            #print "---->"
            self.ProperNameProcessor.init()
            #split the sentence in words
            words = nltk.word_tokenize(sentence)
            tagger = TAGAnalizer()
            
            #print words
            for word in words:
                
                # retira lixo
                #if(len(word) < 2):
                #    continue
                 
                POS = tagger.getTagFromBD(word)
            
            if  POS == 'NPROP':# and self.itsNotRubisProperNoun(word):
                print "------------------------------------------------------------>>>>>"
                #its properNoun
                self.ProperNameProcessor.updateNewName(word,True) 
            else:
                self.ProperNameProcessor.updateNewName(word,False) 
            
            #contar o numero de ocorrencias
            #associar o feeling da frase a esta entidade
            entities = self.ProperNameProcessor.doFinal()
            counting = Counter(entities.values())
            
            
            feeling = self.getFeeling(entities.keys(),sentence)
            
            
            ## TODO descomentar
            # Somar ocorrencias e sentimento da frase
            for (entity,appears) in counting.items():
                if entity not in results:
                    results[entity] = [appears,feeling]
                else:
                    results[entity][0] += appears
                    results[entity][1] += feeling
            
        #Store results
        print results
        return results
        #TODO Check wich entities are recognized officialy
   
   
    def getFeeling(self,entities,sentence):
        return 1
        #TODO ARTUR, para a frase, devolver a pontuacao dela
        
    #This doesnt noun belongs to "blacklist" and it start with capital letter
    def itsNotRubisProperNoun(self,noun):
        if(re.match('[A-Z]',noun) == None):
            return False
        
        noun = noun.lower()
        return len(set([noun]).difference(self.rubishProperNounList)) != 0
    
        
    
    
    
    
    
    
    
    


