'''
Importar a lista de nomes de personalidades, a lista de palavras que nao sao nomes pessoais,
lista de paises e a lista de equivalencias entre palavras para a base de dados
lexicon.db


Created on Mar 25, 2013
'''
import re
from collections import Counter
import sqlite3
import unicodedata
from bs4 import BeautifulSoup
import unicodedata
import codecs
import sqlite3

entitiesDBPath = "../../storage/lexicon.db"
personalitiesDBPath = "../../storage/news.db"

def loadDatabase():
    GetRubish()
    GetNames()
    GetCountries()
    GetEquiv()
    GetThieves()

#######################################################################
#Extracts a name:reputation list and a  proper names list
#######################################################################
def GetNames():
    nomeSet = set()
    file = open("Personalites/input/personalities.txt")
    line = file.readline()
    list = []
    entities = re.split(',',line)
    for word in entities:
        word = word.replace('"',"")
        word = word.replace('"',"")
        entityValue = re.split(":",word)
        name = unicode(entityValue[0])
        value = entityValue[1]
        for nomePart in name.split(" "):
            if nomePart != '' :
                nomeSet.add(nomePart)
                    
        list.append((name,int(value)))

    
    a = sorted(list,key=lambda entry: entry[0])
        
    conn = sqlite3.connect(personalitiesDBPath)     
    c = conn.cursor()       
     
    #print "names"
    #print a
     
    for pair in a:
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(pair[0]).lower()).encode('ASCII', 'ignore'))
        try:
            c.execute('INSERT INTO personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION) values (?,?,?,?)',(unicode(pair[0]),name_norm,pair[1],0))
        except sqlite3.IntegrityError:
            #print "Personalitie exits: "+name_norm
            pass
    
    conn.commit()
    conn.close()
    conn = sqlite3.connect(entitiesDBPath)
    c = conn.cursor()
    #print "ProperNouns"
    #print nomeSet
    for properNoun in nomeSet:
        try:
            name_norm = unicode(unicodedata.normalize('NFKD', unicode(properNoun).lower()).encode('ASCII', 'ignore'))
            c.execute('INSERT INTO properNouns(NOUN) values (?)',[name_norm])
        except sqlite3.IntegrityError:
            pass
   
    conn.commit()
    conn.close()





#######################################################################
# Import common stop words or noun like words
#######################################################################
def GetRubish():
    nomeSet = set()
    file = open("Personalites/input/rubish.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect(entitiesDBPath)     
    c = conn.cursor()       
     
    #print "rubishNames"
    #print nomeSet
    for name in nomeSet:
        name_norm = unicodedata.normalize('NFKD', unicode(name).lower()).encode('ASCII', 'ignore')
        c.execute('INSERT INTO rubishNames(RUBISH_NAME) values (?)',[name_norm])
    conn.commit()
    conn.close()
    
    
    

#######################################################################
#Import countries list
#######################################################################
def GetCountries():
    nomeSet = set()
    file = open("Personalites/input/paises.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect(personalitiesDBPath)     
    c = conn.cursor()       

    #print "countries"
    #print nomeSet
    for name in nomeSet:
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'))
        c.execute('INSERT INTO personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION) values (?,?,?,?)',(unicode(name),name_norm,200,0))
    conn.commit()
    conn.close()
    
    
    
    
#######################################################################
#Import name equivalment list
#######################################################################
def GetEquiv():
    nomeSet = set()
    file = open("Personalites/input/equivalent.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect(entitiesDBPath)     
    c = conn.cursor()       

    #print "equiv"
    #print nomeSet
    for name in nomeSet:
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'))
        n = name_norm.split(":")
        c.execute('INSERT INTO nameEquiv(NAME,EQUIV) values (?,?)',(unicode(n[0]),unicode(n[1])))
    conn.commit()
    conn.close()

############################################################################
#Este modulo realiza o parsing da pagina da assembleia da repulbica
#em que consta a lista de todos os deputados e faz upload desta lista para a base de dados
#associando a cada entidade o respectivo partido politicos como deputados.
############################################################################
def GetThieves():
    file = codecs.open("Personalites/input/deputados.html","r")
    doc = str(file.readlines())   
    soup = BeautifulSoup(doc)
    
    #print "download"
    #os a com href que contem biografia
    def cond(x):
        if x:
            return str(x).find("Biografia") != -1
        else:
            return False
        
    listaDeputados = []
    rows = soup.findAll('a', {'href': cond})
    
    for entry in rows:
        entry = entry.text.decode('string-escape').decode("utf-8")
        listaDeputados.append((entry));
        
    #sacar partido
    #CDS-PP PS PSD PCP BE PEV
    #os a com href que contem biografia
    
    
    def isPartido(link):
        if link == "PS":
            return True
        if link == "CDS-PP":
            return True
        if link == "PSD":
            return True
        if link == "PCP":
            return True
        if link == "BE":
            return True
        if link == "PEV":
            return True
        return False
        
        
    rows = soup.findAll('span')
    
    i = 0
    result = []
    for link in rows:
        link = link.text
        if isPartido(link):
            result.append([listaDeputados[i],link])
            i += 1
        
    #result: [ [u'PassosCoelho':'PSD],u'borrego','PCP'}
    
    #Import to database
    conn = sqlite3.connect(personalitiesDBPath)     
    c = conn.cursor()  
    #print result
    for entry in result:
        name = entry[0]
        partido = entry[1]
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(name).lower()).encode('ASCII', 'ignore'))
        try:   
            c.execute('INSERT into personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION,PARTIDO,GOVERNO) values(?,?,?,?,?,?)',[name,name_norm,'1000','20',partido,''])
        except:
            c.execute('UPDATE personalities set PARTIDO=? where NAME_NORM=?',[partido,name_norm])
        #print entry
        
        
    
    
    ############# Government list #############################
    f = open("Personalites/input/governo.txt")
    for governante in f:
        name = unicode(governante.split(":")[0])
        adjuntancy = unicode(governante.split(":")[1])
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(name).lower()).encode('ASCII', 'ignore'))
        try:   
            c.execute('INSERT into personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION,PARTIDO,GOVERNO) values(?,?,?,?,?,?)',[name,name_norm,'1000','20','PSD',adjuntancy])
        except:
            c.execute('UPDATE personalities set GOVERNO=?, PARTIDO=? where NAME_NORM=?',[adjuntancy,'PSD',name_norm])        
    conn.commit()
    conn.close()


