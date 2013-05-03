'''
Created on May 1, 2013
'''
import sqlite3
import unicodedata
from operator import itemgetter, attrgetter

class ProperNameProcessor:
    __dBLocation = "../entities.db"
    def __init__(self):
        self.conn = sqlite3.connect(self.__dBLocation)     
        self.__cursor = self.conn.cursor() 
        self.knowEntities = self.LoadKnownEntitiesToMemory()
        self.stopWords = ['dos','das','de','do','da']
        self.stopWord = ""
        self.nameEquiv = self.LoadKnownEquivalentsToMemory()
        
    def init(self):
        self.properNounCandidate = ""
        self.nameBuilder = ""
        self.unknownEntities = []
        self.AcceptedProperNounCandidates = []
        self.conn = sqlite3.connect(self.__dBLocation)     
        self.__cursor = self.conn.cursor() 
        
    #Recebe um nome
    def updateNewName(self,name,proper):        
        #Apanhar palavras separadas por .
        for name in name.split("."):
            #self.nounColletingMode(name,proper)
            self.restrictMode(name,proper)
    
    
    #Confia no facto de ser proper ou nao e com base nisso gera os nomes
    def restrictMode(self,name,proper):
        if proper: 
                if(self.stopWord != ""):
                    self.nameBuilder += self.stopWord + " "
                    self.stopWord = ""
                self.nameBuilder += name + " "
        else:
            #Its not a proper name 
            if name in self.stopWords and self.nameBuilder != "":
                self.stopWord = name
            else:
                #Terminar a concatenacao and clean state
                self.finishNameBuilding()
                
                
    def nounColletingMode(self,name,proper):
        if proper:
            if(self.stopWord != ""):
                    self.nameBuilder += self.stopWord + " "
                    self.stopWord = ""
                    
            if self.properNounCandidate != "":
                #Im the next name so it is a noun
                self.nameBuilder += self.properNounCandidate
                self.confirmProperNounCandidate() 
                
            #if pertence a  tabela de ProperNoun, concatenar 
            if self.isKnownProperNoun(name):
                self.nameBuilder += name + " "
                return
            else:
                #save as properNounCandidate, se o proximo for nome, este passa de candidato a fixo
                self.properNounCandidate = name
        else:
            #Its not a proper name 
            self.properNounCandidate = ""
            if name in self.stopWords and self.nameBuilder != "":
                self.stopWord = name
            else:
                #Terminar a concatenacao and clean state
                self.finishNameBuilding()
    
    
    
    def doFinal(self):
        #Save the pendent name
        self.finishNameBuilding()
        result = self.ProcessEntities()
        self.conn.commit()
        self.conn.close()
        return result

    #Parameter: entites = ["dario","artur"]
    def ProcessEntities(self):
        # print "Known Entities:"
        unknownEntities = self.unknownEntities
        #print unknownEntities
        result = dict()
        for unknownEntity in unknownEntities:
            #Check if it match any known entity
            candidates = []
            try:
                unknownEntityOrg = str(unknownEntity)
            except UnicodeEncodeError:
                unknownEntityOrg = str(unicode(unknownEntity.encode('utf8')))
            
            unknownEntity = unknownEntityOrg.lower()
            unknownEntity_norm = unicode(unicodedata.normalize('NFKD', unicode(unknownEntity).lower()).encode('ASCII', 'ignore'))
            #Procurar entidade equivalente
            unknownEntity_norm = self.checkEquivalent(unknownEntity_norm)
            
            
            for entity in self.knowEntities:
                    #NAME,NAME_NORM,,REPUTATION,PRE_REPUTATION
                    known_name = str(entity[1]).lower()
                    #how percent of name1 must be contanined by name2?
                    #normalizar o nome da entidade
                    
                    if(self.NameIsContained(unknownEntity_norm,known_name)):
                        #print "Known Entity: "+entity[0]+" famous level: "+str(entity[3])+", reputation: "+str(entity[2])                        
                        candidates.append([entity[0],entity[2],entity[3]])
            
            if len(candidates) == 0:
                self.newEntity(unknownEntityOrg)
                #print "new entiry:"+unknownEntityOrg
                result[unknownEntityOrg] = unknownEntityOrg
            else:
                bestCandidate = self.selectBestCandidate(unknownEntity,candidates)
                #print "Original: "+unknownEntityOrg+" best candidate: "+bestCandidate[0]
                result[unknownEntityOrg] = bestCandidate[0]
        return result
            
            
    
    #Ver se todo o nome esta contido dentro do outro
    def NameIsContained(self,name1,name2):
        names1 = set(name1.split(" "))
        names2 = set(name2.split(" "))
        
        #cast to get names1 < name2
        if len(names1) > len(names2):
            names3 = names1
            names1 = names2
            names2 = names3
        
        diff = names1.difference(names2)
        if len(diff) == 0:
            return True
        return False;
    
    
    
    
    def LoadKnownEntitiesToMemory(self):
        result = []

        for row in self.__cursor.execute("Select NAME,NAME_NORM,PRE_REPUTATION,REPUTATION from personalities"):
            result.append([row[0],row[1],row[3],row[2]]) 
        return result
    

    
    def isKnownProperNoun(self,noun):
        resultsCount = self.__cursor.execute("Select * from properNouns where NOUN = ?",[noun.lower()]).rowcount
        if resultsCount == 0:
            return False
        return True 

        
    #New noun to add to database
    def confirmProperNounCandidate(self,noun):
        self.__cursor.execute('INSERT INTO properNouns(NOUN) values (?)',[unicode(noun).lower()])
        self.properNounCandidate = ""
        
    def finishNameBuilding(self):
        if(self.nameBuilder == ""):
            return
        self.unknownEntities.append(self.nameBuilder[:-1])
        self.properNounCandidate = ""
        self.nameBuilder = ""
        self.stopWord = ""
        
    #Select the best match candidate
    def selectBestCandidate(self,unkown,candidates):
        #candidates[i][0] name
        #candidates[i][1] news reputation
        #canditates[i][2] pre-reputation
        
        #BEST matching
        #sort by reputation and pre-reputation
        candidates = sorted(candidates, key=itemgetter(1,2), reverse=True);
        #print candidates
        candidates[0][1] += 1
        #print candidates[0]
        return candidates[0]
        
    #Adicionar esta entidade a base de dados
    def newEntity(self,entityName):
        #print "New entity: "+entityName
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(entityName).lower()).encode('ASCII', 'ignore'))
        try:
            self.__cursor.execute('INSERT INTO personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION) values (?,?,?,?)',(unicode(entityName),name_norm,0,1))
        except sqlite3.IntegrityError:
            pass
        self.knowEntities.append([unicode(entityName),1,0])


    def LoadKnownEquivalentsToMemory(self):
        result = []
        for row in self.__cursor.execute("Select NAME,EQUIV from nameEquiv"):
            result.append([row[0],row[1]]) 
        return result
    
    def checkEquivalent(self,name):
        #name|equiv
        for pair in self.nameEquiv:
            if pair[0] == name:
                return pair[1]
        return name
        
        
"""        
a = ProperNameProcessor()
a.init()
a.updateNewName("Gilberto",True) 
#a.updateNewName("Silva",True) 
a.doFinal() """ 