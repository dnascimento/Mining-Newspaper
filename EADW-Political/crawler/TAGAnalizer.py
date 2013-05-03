import re
import unicodedata
import os
import sqlite3


class TAGAnalizer:
    
    TagFile = "../sentimentsBase/in/TagFile.txt"

    def __init__(self):
        print "Carregando LIB TAG Libs"
        TagFileDict = self.loadDictionary(self.TagFile)
        print self.TagFileDict
        #TagNomeDict = self.loadDictionary(self.TagNomes)
        print "Done Loading Libs"

        



    def loadDictionary(self,Filename):
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
    
    def AddProperNounsFromDatabaseFile(self):    
        f = open("out/dbProperNouns.txt","r")
        outWord = open("out/lexiconWords.txt","a")
        
        for row in f:
            word = unicode(row[:-1]) 
            name_norm = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))
            if name_norm in self.wordWritedSet:
                print "exists: "+name_norm
                #TODO Verificar se ao existir, e um nome proprio ou nao
                continue 
            meta = "NPROP"
            outWord.write(word+":"+meta+":"+":"+"\n")
        
        outWord.close()
        os.remove("out/dbProperNouns.txt")
    
    
    # procura o tipo de palaver no dicionario
    # se nao encontrar tenta com letra pequena
    def getTagFile(self, word):
        fullTag = self.TagFileDict.get(word)
        if(isinstance(fullTag, type(None))):
            fullTag = self.TagFileDict.get(word.lower())
            if(isinstance(fullTag, type(None))):
                return 'null'
            else:
                return fullTag
        else:
            return fullTag
        
    def getTagDB(self, word):
        print "db"
    
#print floresta.tagged_words()
#mac_morphoDict = dict(mac_morpho.tagged_words())
x = TAGAnalizer()
