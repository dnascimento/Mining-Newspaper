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

#cria uma lista com a tag em causa
for i in range(0,len(negtxt)):
    neglist.append('negative')

#igual ao anterior
for i in range(0,len(postxt)):
    poslist.append('positive')

#Cria tuplos, especifica tag
postagged = zip(postxt, poslist)
negtagged = zip(negtxt, neglist)


# Combina Tudo
taggedTotal = postagged + negtagged


tweets = []

#Create a list of words in the tweet, within a tuple.
for (word, sentiment) in taggedTotal:
    word_filter = [i.lower() for i in word.split()]
    tweets.append((word_filter, sentiment))

#Pull out all of the words in a list of tagged tweets, formatted in tuples.
def getwords(tweets):
    allwords = []
    for (words, sentiment) in tweets:
        allwords.extend(words)
    return allwords

#Order a list of tweets by their frequency.
def getwordfeatures(listoftweets):
    #Print out wordfreq if you want to have a look at the individual counts of words.
    wordfreq = nltk.FreqDist(listoftweets)
    words = wordfreq.keys()
    return words

#Calls above functions - gives us list of the words in the tweets, ordered by freq.
print getwordfeatures(getwords(tweets))

wordlist = [i for i in wordlist if not i in stopwords.words('english')]
wordlist = [i for i in wordlist if not i in customstopwords]

def feature_extractor(doc):
    docwords = set(doc)
    features = {}
    for i in wordlist:
        features['contains(%s)' % i] = (i in docwords)
    return features

#Creates a training set - classifier learns distribution of true/falses in the input.
training_set = nltk.classify.apply_features(feature_extractor, tweets)






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