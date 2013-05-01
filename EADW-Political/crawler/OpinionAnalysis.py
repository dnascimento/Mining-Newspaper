#!/usr/bin/python
import nltk.classify.util, nltk.metrics
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



#ADJ(ective), N(oun), V(erb) and IDIOM), and
#Polarity (POL), which can be positive (1), negative (-1) or neutral (0);
#Some entries also include an additional code (REV), which refers to specific notes included by the annotator. At this point, we can find the following notations:



fileName = "/home/artur-adm/teste/SentiLex-flex-PT03.txt"
#fileName = "/home/artur-adm/teste/SentiLex-flex-PT03.txt"

positive = set()
negative = set()

lex = open(fileName, "r")
for line in lex:
    #print line
    palavras = line.split('.')[0].split(',')
    pos = line.split('Po')[1].split('=')[1].split(';')[0]
    polarity = int(line.split('POL:N')[1].split('=')[1].split(';')[0])
    
    #print len(palavras),
    #    print line
    
    #print pos, polarity, palavras

    if(polarity > 0):
        positive.update(palavras)
    else:
        negative.update(palavras)
        
#print "Pos", positive
#print "Neg", list(negative)[:100]



#nltk.download()



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