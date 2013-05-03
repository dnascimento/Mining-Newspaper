'''
Created on May 3, 2013
'''
import re
import unicodedata
import os
import sqlite3

class Parser:
    wordWritedSet = set()
    
    def SentiFlexProcess(self):
        file = open('in/SentiLex-flex-PT03.txt')
        
        outExpression = open("out/lexiconExpressions.txt","w+")
        outWord = open("out/lexiconWords.txt","w+")
        
        for linha in file:
            line = unicode(linha[:-1])
            #separar palavras e metadados
            lineSplit = line.split(".")
            
            #separar palavras_frases
            sentences = lineSplit[0].split(',')
            
            #extrair os metadados
            meta = lineSplit[1]
            
            #POS
            match = re.search("PoS=[a-zA-Z]+",meta)
            try:
                POS = match.group(0).replace("PoS=","")
            except AttributeError:
                print "POS Pass:"+meta
                pass
            
            #Sexo
            Sex = ""
            if POS == "Adj":
                #print "try: "+meta
                match = re.search("FLEX=[a-zA-Z]+",meta)
                try:
                    Sex = match.group(0).replace("FLEX=","")
                except AttributeError:
                    print "SEX Pass:"+meta
                    pass
            
            
            #Opinions
            opinions = re.findall("POL:N\d=-?\d+",meta)
            
            i = 0

    
            for sentence in sentences:
                    name_norm = unicode(unicodedata.normalize('NFKD', unicode(sentence).lower()).encode('ASCII', 'ignore'))
                    if name_norm in self.wordWritedSet:
                        continue
                    
                    if len(sentence.split(" ")) > 1:
                        out = outExpression
                    else:
                        out = outWord
                        
                    if len(opinions) == 0:
                        result = sentence+":"+POS+":"+":"+Sex
                    else:
                        result = sentence+":"+POS+":"+opinions[i].split("=")[1]+":"+Sex
                        if i < (len(opinions) - 1):
                            i += 1
                            
                    print result
                    out.write(result+"\n")
                    self.wordWritedSet.add(name_norm)
                    
        outWord.close()            
        outExpression.close()
        file.close()     
    
    
    def TagFileProcess(self):
        file = open('in/TagFile.txt')
        outWord = open("out/lexiconWords.txt","a")
        
        for linha in file:
            line = unicode(linha[:-1])
            #separar palavras e metadados
            lineSplit = line.split(":")
            word = lineSplit[0]
            
            name_norm = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))
            if name_norm in self.wordWritedSet:
                continue
                
            meta = lineSplit[1]
            #start by common text
            if  re.match('^([a-zA-Z])+',word) == None:
                continue
            
            if meta == "ADJ":
                meta = "Adj"
            if meta == "NUM":
                continue
            if meta == "N|DAT":
                continue
                    
            result = word+":"+meta+":"+":"
            outWord.write(result+"\n")
            print result
            self.wordWritedSet.add(name_norm)

    def SortFileLines(self):
        f = open('out/lexiconWords.txt',"r")
        # omit empty lines and lines containing only whitespace
        lines = [line for line in f if line.strip()]
        f.close()
        os.remove('out/lexiconWords.txt')
        lines.sort()
        f = open('out/lexiconWords.txt',"w+")
        f.writelines(lines)
        
        
        
    #converter a tabela properNouns do entities para ficheiro para ser limpa manualmente
    def SaveDatabaseProperNounsToFile(self):
        out = open("dbProperNouns.txt","w+")
        self.__conn = sqlite3.connect("../entities.db")     
        self.__cursor = self.__conn.cursor()   
        for row in self.__cursor.execute("Select * from properNouns"):
            out.write(row[0])
        out.close()
        
    def AddProperNounsFromDatabaseFile(self):    
        f = open("dbProperNouns.txt","r")
        outWord = open("out/lexiconWords.txt","a")
        
        for row in f:
            word = unicode(row[:-1]) 
            name_norm = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))
            if name_norm in self.wordWritedSet:
                continue 
            meta = "NPROP"
            outWord.write(word+":"+meta+":"+":")
        
        outWord.close()
            
            
            
parser = Parser()   
parser.SentiFlexProcess()  
parser.TagFileProcess()
parser.SortFileLines()

