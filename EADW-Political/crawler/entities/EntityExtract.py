'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''

#import nltk
import nltk
from nltk.corpus import floresta
from pprint import pprint
import  WordProcessor
import sqlite3
import re
from collections import Counter
#Ler cada um dos textos nao processados
#Realizar a analise com o NLTK


class EntityExtractor:
    def __init__(self):
        self.ProperNameProcessor = WordProcessor.ProperNameProcessor()
        self.rubishProperNounList = self.LoadRubishList()
        
    def ParseEntitiesFromDoc(self,doc):
        self.ProperNameProcessor.init()
        #split the doc in sentences
        sent_tokenizer=nltk.data.load('tokenizers/punkt/portuguese.pickle')
        
        
        
        entities = []
        #sentences = nltk.sent_tokenize(doc)
        sentences = sent_tokenizer.tokenize(doc)
        for sentence in sentences:
            #split the sentence in words
            words = nltk.word_tokenize(sentence)
            #PostOfSpeak (sintax) analysis [('dario',EN),('artur','en')]
            tagger = nltk.data.load(nltk.tag._POS_TAGGER)
            
            taggedWords = tagger.tag(words)
            
            #Convert to tree
            ne_tree = nltk.ne_chunk(taggedWords,binary=False) 
            #Aplicar um classifier
            
            #Vamos procurar entidades
            
            
            for n in ne_tree.leaves():
                if (n[1] == "NNP") & self.itsNotRubisProperNoun(n[0]) :
                    #its properNoun
                    self.ProperNameProcessor.updateNewName(n[0],True) 
                else:
                    self.ProperNameProcessor.updateNewName(n[0],False) 
            
            
        entities = self.ProperNameProcessor.doFinal()
        return Counter(entities)
            #Check wich entities are recognized officialy
   
   
    #This doesnt noun belongs to "blacklist" and it start with capital letter
    def itsNotRubisProperNoun(self,noun):
        if(re.match('[A-Z]',noun) == None):
            return False
        
        noun = noun.lower()
        return len(set([noun]).difference(self.rubishProperNounList)) != 0
    
    def LoadRubishList(self):
        conn = sqlite3.connect("entities.db")
        cursor = conn.cursor() 
        lista = []

        for row in cursor.execute("Select * from rubishNames"):
            lista.append(row[0]) 
        conn.commit()
        conn.close()
        return lista

#EntityExtractor().ParseEntitiesFromDoc(str(u"Desde 1919 que Cristiano Ronaldo, o Seguro, Gaspar e o Coelho o Dario Nascimento e bom jogador do benfica. Os Sportiguistas estao com a azia do Capela"))                          




