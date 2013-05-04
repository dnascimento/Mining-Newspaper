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