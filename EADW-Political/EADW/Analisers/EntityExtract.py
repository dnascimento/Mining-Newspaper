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
    
    __dBLexiconLocation = "../storage/lexicon.db"
    lixo  = nltk.corpus.stopwords.words('portuguese')
    opinionAnalist = Opinion()

    ########################################################
    #Load rubish names list and init properNameProcessor
    #########################################################
    def __init__(self):
        self.ProperNameProcessor = WordProcessor.ProperNameProcessor()
        conn = sqlite3.connect(self.__dBLexiconLocation)
        cursor = conn.cursor()
        self.rubishProperNounList = []
        for row in cursor.execute("Select * from rubishNames"):
            self.rubishProperNounList.append(row[0]) 
        conn.close()
               
        
        
    ########################################################
    #Parse the doc, get entities, analysis etc
    ########################################################
    def ParseEntitiesFromDoc(self,url,doc):
        
        self.ProperNameProcessor.init()
        results = dict()
        sentences = nltk.sent_tokenize(doc.decode("utf8"))
                    
        for sentence in sentences:
            
            self.ProperNameProcessor.init()
            
            # Remove Pontuacoo
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
            
            feelingAndAbjectives = self.opinionAnalist.getSentenceOpinion(sentence)
            feeling = feelingAndAbjectives[0]
            adjectives = feelingAndAbjectives[1]
            # TODO Dario Usar os Ajectivos
            
            # Somar ocorrencias e sentimento da frase
            for (entity,appears) in counting.items():
                if entity not in results:
                    results[entity] = [appears,feeling]
                    print entity, feeling
                else:
                    results[entity][0] += appears
                    results[entity][1] += feeling
            
        return results
   
   
   
   
    
    
    
    
    
    
    


