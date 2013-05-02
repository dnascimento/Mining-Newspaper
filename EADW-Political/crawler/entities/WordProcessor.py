'''
Created on May 1, 2013
'''
import sqlite3
from operator import itemgetter, attrgetter

class ProperNameProcessor:
    __dBLocation = "../entities.db"
    def __init__(self):
        self.conn = sqlite3.connect(self.__dBLocation)     
        self.__cursor = self.conn.cursor() 
        self.knowEntities = self.LoadKnownEntitiesToMemory()
        self.stopWords = ['dos','das','de','do','da']
        
    def init(self):
        self.properNounCandidate = ""
        self.nameBuilder = ""
        self.unknownEntities = []
        self.AcceptedProperNounCandidates = []
        self.conn = sqlite3.connect(self.__dBLocation)     
        self.__cursor = self.conn.cursor() 
        
    #Recebe um nome
    def updateNewName(self,name,proper):
        self.nounColletingMode(name,proper)
 
    
    
    #Apenas se pertencer a tabela de nomes conhecidos ou for stopword
    def restrictMode(self,name,proper):
        if proper and self.isKnownProperNoun(name):
                self.nameBuilder += name + " "
        else:
            #Its not a proper name 
            if name in self.stopWords and self.nameBuilder != "":
                self.nameBuilder += name + " "
            else:
                #Terminar a concatenacao and clean state
                self.finishNameBuilding()
                
                
    def nounColletingMode(self,name,proper):
        if proper:
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
                self.nameBuilder += name + " "
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
                continue
            unknownEntity = str(unknownEntity).lower()
            for entity in self.knowEntities:
                    known_name = str(entity[0]).lower()
                    #how percent of name1 must be contanined by name2?
                    if(self.NameIsContained(known_name,unknownEntity)):
                        #print "Known Entity: "+entity[0]+" famous level: "+str(entity[1])+", reputation: "+str(entity[2])                        
                        candidates.append([entity[0],entity[1],entity[2]])
            
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

        for row in self.__cursor.execute("Select * from personalities"):
            result.append([row[0],row[2],row[1]]) 
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
        self.__cursor.execute('INSERT INTO personalities(NAME,PRE_REPUTATION,REPUTATION) values (?,?,?)',(unicode(entityName),0,1))
        self.knowEntities.append([unicode(entityName),1,0])


        
        
"""        
a = ProperNameProcessor()
a.init()
a.updateNewName("Gilberto",True) 
#a.updateNewName("Silva",True) 
a.doFinal() """ 