#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
#nltk.download()

class Opinion():
    
    dbpath = "../storage/lexicon.db"
    
    
    # Devolve o tipo de Palavra e a sua opiniao, +-1
    def getWordInfluence(self,word):
        conn = sqlite3.connect(self.dbpath)     
        c = conn.cursor()
        c.execute('SELECT POS,OPINION FROM lexicon WHERE OPINION IS NOT NULL AND WORD=?', [word])
        res = c.fetchall()
        conn.commit()
        conn.close()
        return res
    
    # Devolve um tuplo composto por um valor que indicar se a frase é positiva ou negativa
    # o valor é positivo se a opiniao for positiva, negativo caso contrario, o segundo campo
    # inclui uma lista de adjectivo que aparece na frase
    def getSentenceOpinion(self, sentence):
        
        words = sentence.split(" ")
        adjectives = []
        positive = 0;
        negative = 0;
        
        for word in words:
            res = self.getWordInfluence(word)
            if(len(res) > 0):
                # Guardar Adj
                if("Adj" in res[0][0]):
                    adjectives.append(word)
                    
                if res[0][1] is not None:
                    if res[0][1] == 1:
                        positive += 1
                    elif res[0][1] == -1:
                        negative += 1
                                 
        return positive - negative, adjectives
                
        


#o = Opinion()
#fraseboa = u" ola esta frase tem coisas boas e server para dar demonstrar a boa eficacia do nosso algoritmo que é muito sofisticado"
#frasema = u"bater no governo é como as bestas do parlamento assustam o povo"
#print o.getSentenceOpinion(fraseboa)
#print o.getSentenceOpinion(frasema)



