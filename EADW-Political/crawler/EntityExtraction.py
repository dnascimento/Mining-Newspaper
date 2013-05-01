'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''


import nltk
from pprint import pprint
import ParseFileNames
#Ler cada um dos textos nao processados
#Realizar a analise com o NLTK

def ParseEntitiesFromDoc(doc):
    knowEntities = ParseFileNames.GetNames()
    #split the doc in sentences
    sentences = nltk.sent_tokenize(doc)
    #split the sentence in words
    words = nltk.word_tokenize(sentences[0])
    #PostOfSpeak (sintax) analysis [('dario',EN),('artur','en')]
    taggedWords = nltk.pos_tag(words)
    
    #Convert to tree
    ne_tree = nltk.ne_chunk(taggedWords,binary=False) 
    #Aplicar um classifier
    
    #Vamos tirar apenas os nomes e procurar entidades
    #NNP - noun proper  
    #NNPS - noun proper plural
    
    
    #Foreach entity, process the opinion
    #OpinionAnalysis(entity,...)
    entities = []
    for n in ne_tree:
        if isinstance(n, nltk.tree.Tree):               
            if n.node == 'PERSON':
                name = ""
                for namePart in n:
                    name += namePart[0]+" "
                entities.append(name)
                
    print entities
    
    
    #Check wich entities are recognized officialy
    for new_entity in entities:
        new_name = str(new_entity).replace(" ","").lower()
        for entity in knowEntities:
            known_name = str(entity[0]).replace(" ","").lower()
            #TODO Fazer a percentagem das frase para tolerar nomes incompletos
            if(known_name == new_name):
                print "Known Entity: "+entity[0]+" famous level: "+str(entity[1])
            if(known_name > new_name):
                break
                      
#ParseEntitiesFromDoc(str("O Aaron Swartz, Dario Nascimento, Ze Carlitos e o Artur ja foi jogador do Benfica mas ambos tem um Opel Corsa e um Audi A3. Os Sportiguistas estao com a azia do Capela"))