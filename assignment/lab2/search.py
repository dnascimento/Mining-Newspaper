'''
Created on Feb 27, 2013

@author: darionascimento
'''
import re
import sys
import math

def readDoc(docFile):
    invertIndex = {}
    docIndex = 0
    totalWords = 0
    
    file = open(docFile,'r');
    
    for line in file:
        docIndex += 1
        #parse to read word by word
        words = re.split('\W+',line)
        for word in words:
            totalWords += 1
            if word == '':
                continue
            
            #add to invert index
            if word not in invertIndex:
                invertIndex[word] = {}
            
            tf = invertIndex[word]
            
            if docIndex in tf:
                tf[docIndex] += 1
            else:
                tf[docIndex] = 1

    indexStruct = {'index':invertIndex, 'totalDoc':docIndex,'totalWords':totalWords,'totalUniqueWords': len(invertIndex)}
    print indexStruct
    return indexStruct


#Ex2
def queryInterface(indexStruct):
    var = raw_input("Enter your terms: ")
    print "you entered ", var
    
    words = re.split('\W+',var)
    for word in words:
        getStatistics(word,indexStruct)

#Ex2
def getStatistics(word,indexStruct):
    invertIndex = indexStruct['index']
    
    tf =  invertIndex[word]
    df = len(tf)

    
    print "df: "+str(df)
    
    lo,hi = sys.maxint,-sys.maxint-1
    for x in invertIndex[word].values():
        if x < lo:
            lo = x
        if x > hi:
            hi = x
    
    print "Min Freq: "+str(lo)
    print "Max Freq: "+str(hi)

    N = indexStruct['totalDoc']
    
    print "IDF: "+str(math.log(N/df))
    
############################ Ex 3 ###########################################
def queryInterface3(indexStruct):
    var = raw_input("Enter your terms: ")
    print "you entered ", var
    
    A = {}

    words = re.split('\W+',var)
    for word in words:
        dotProduct(word,indexStruct,A)
    
    print "Not sort results: "
    print A
    A = sorted(A.keys(), key=A.__getitem__)
    print "Sorting...."
    print A
        
#ex3
def dotProduct(word,indexStruct,A):
    
    it = indexStruct['index'][word]
    df = len(it)
    N = indexStruct['totalDoc']
    idf = math.log(N/df)
    
    print "IDF: "+str(idf)
     
    for doc, freq in it.iteritems():
        if doc not in A:
            A[doc] = 0
        
        A[doc] = A[doc] + freq*idf
        
    
    
    
    
    
    

index = readDoc("data.txt") 
queryInterface3(index)            
                        
            
                