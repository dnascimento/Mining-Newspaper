#!/usr/bin/python
import nltk.classify.util, nltk.metrics
from nltk.corpus import stopwords
from nltk.corpus import floresta
from nltk.corpus import mac_morpho
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import toolbox
from urllib import urlopen
import collections, itertools
import datetime
import nltk
import nltk.classify.util, nltk.metrics
import os
import pickle
import re
#nltk.download()

customstopwords = ['a', 'de', 'e']

p = open('positive.txt', 'r')
n = open('negative.txt', 'r')

postxt = p.read().split(":")
negtxt = n.read().split(":")


neglist = []
poslist = []

#Create a list of 'negatives' with the exact length of our negative tweet list.
for i in range(0,len(negtxt)):
    neglist.append('negative')

#Likewise for positive.
for i in range(0,len(postxt)):
    poslist.append('positive')

#Creates a list of tuples, with sentiment tagged.
postagged = zip(postxt, poslist)
negtagged = zip(negtxt, neglist)


# Combina Tudo
taggedTotal = postagged + negtagged


print postagged








def loadDictionary(Filename):
    list = []
    f = open(Filename, "r")
    for line in f:
        key = line.split(":")[0]
        value = line.split(":")[1]
        if(len(line.split(":"))>2):
            value = line.split(":")[2]
        if('\n' in value):
            value = value.split('\n')[0]
        list.append([key, value])
    f.close()
    return dict(list)


# procura o tipo de palaver no dicionario
# se nao encontrar tenta com letra pequena
def getTag( word ):
    fullTag = mac_morphoDict.get(word)
    if(isinstance(fullTag, type(None))):
        fullTag = mac_morphoDict.get(word.lower())
        if(isinstance(fullTag, type(None))):
            return 'null'
        else:
            return fullTag
    else:
        return fullTag

#print floresta.tagged_words()
#mac_morphoDict = dict(mac_morpho.tagged_words())
print "Carregando LIB"
mac_morphoDict = loadDictionary("TagFile")



text = "Artur Balanuta e um rapaz muito Feliz. Antnio Reis amarelo verde carro partiu . triste Dario menina."
#text = "Artur Balanuta rapaz"
frases = nltk.sent_tokenize(text)
for frase in frases:
    
    #print frase
    tokens = nltk.word_tokenize(frase)
    for token in tokens:
        tag = getTag(unicode(token))
        print token, tag






#print frases[0]
#palavras = nltk.word_tokenize(text)
#print palavras
#pos_tag = nltk.pos_tag(palavras)
#print pos_tag

#ne = nltk.ne_chunk(pos_tag, binary=True)
#print ne.split('NE')


#text = nltk.word_tokenize("They refuse to permit us to obtain the refuse permit")
#print nltk.pos_tag(text)




#url = "http://www.sol.pt/inicio/Internacional/Interior.aspx?content_id=74108"
#html = urlopen(url).read()

#raw = nltk.clean_html(html)
#tokens = nltk.wordpunct_tokenize(raw)
#text =  nltk.Text(tokens)
#text.concordance('gene')
#print tokens
#print text




#corpus_root = "/home/artur-adm/teste/SentiLex-flex-PT03.txt"
#wordlists = PlaintextCorpusReader(corpus_root, '.*')
#print wordlists

#print toolbox.entries("rotokas.dic")

#nltk.download()
#print floresta








#class OpinionAnalysis(Thread):         
#    
#    def __init__(self, entitiesList,wordsTree):
#        self.__entitiesList = entitiesList;
#        self.__wordsTree = wordsTree;
#        
#    def ProcessOpinion(self,EntitiesList,WordsTree):
#        print "TODO"