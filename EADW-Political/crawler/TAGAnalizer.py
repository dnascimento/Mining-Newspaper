from nltk.corpus import mac_morpho
import re
import unicodedata
import os
import sqlite3


class TAGAnalizer:
    
    TagFile = "../sentimentsBase/in/TagFile.txt"
    TagDBPath = "../tags.db"
        
    def loadToDB(self):
        
        # Apag BD antiga
        if os.path.exists(self.TagDBPath):
            os.remove(self.TagDBPath)
        
        # Cria BD nova
        conn = sqlite3.connect(self.TagDBPath)     
        c = conn.cursor()
        c.execute('CREATE TABLE tags (WORD TEXT  NOT NULL,TAG TEXT  NOT NULL ,Primary Key(WORD))')
            
            
        # Carega o ficheiro para a BD
        fd = open(self.TagFile, 'r')
        for line in fd:
            word = line.split(":")[0]
            tag  = line.split(":")[1].split("\n")[0]
            
            if '|' in tag:
                tag = tag.split('|')[0]
                
            # Normalize
            word = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))    
            tag = unicode(tag)
            
            try:
                c.execute('Insert into tags(WORD,TAG) values(?,?)',(word,tag))
            except sqlite3.IntegrityError:
                pass
                
        # Fecha Coneccoes
        conn.commit()
        conn.close() 
        fd.close()
        
        
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
    
    # devolve o valor da tag a partir da BD           
    def getTagFromBD(self, word):
        #Normalize
        word = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))
        
        # Liga a BD
        conn = sqlite3.connect(self.TagDBPath)     
        c = conn.cursor()
        c.execute('SELECT TAG FROM tags WHERE WORD = ?', [word])
        result = c.fetchone()
        conn.close()
        
        if(isinstance(result, type(None))):
            return str(unicode('null'))
        else:
            return result[0]
    
    #def AddProperNounsFromDatabaseFile(self):    
    #    f = open("out/dbProperNouns.txt","r")
    #    outWord = open("out/lexiconWords.txt","a")
    #    
    #    for row in f:
    #        word = unicode(row[:-1]) 
    #        name_norm = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))
    #        if name_norm in self.wordWritedSet:
    #            print "exists: "+name_norm
    #            #TODO Verificar se ao existir, e um nome proprio ou nao
    #            continue 
    #        meta = "NPROP"
    #        outWord.write(word+":"+meta+":"+":"+"\n")
    #    
    #    outWord.close()
    #    os.remove("out/dbProperNouns.txt")
    
    
    # procura o tipo de palaver no dicionario
    # se nao encontrar tenta com letra pequena
    #def getTagFile(self, word):
    #    fullTag = self.TagFileDict.get(word)
    #    if(isinstance(fullTag, type(None))):
    #        fullTag = self.TagFileDict.get(word.lower())
    #        if(isinstance(fullTag, type(None))):
    #            return 'null'
    #        else:
    #            return fullTag
    #    else:
    #        return fullTag
                
                
                

