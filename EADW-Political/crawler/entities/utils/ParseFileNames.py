'''
Created on Mar 25, 2013
'''
import re
from collections import Counter
import sqlite3
import unicodedata


#
#Extracts a name:reputation list and a  nomial names list
#
def GetNames():
    nomeSet = set()
    file = open("personalities.txt")
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
    
        
    conn = sqlite3.connect("../../../entities.db")     
    c = conn.cursor()       
    c.execute('''CREATE TABLE personalities (NAME text primary key, NAME_NORM text, PRE_REPUTATION INTEGER, REPUTATION INTEGER)''')
    c.execute('delete from personalities')
    c.execute('''CREATE TABLE properNouns (NOUN text primary key)''')
    c.execute('delete from properNouns')
    c.execute('''CREATE TABLE nameEquiv (NAME text,EQUIV text)''')

     
    print "names"
    print a
     
    for pair in a:
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(pair[0]).lower()).encode('ASCII', 'ignore'))
        c.execute('INSERT INTO personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION) values (?,?,?,?)',(unicode(pair[0]),name_norm,pair[1],0))
    
    print "ProperNouns"
    print nomeSet
    for properNoun in nomeSet:
        try:
            name_norm = unicode(unicodedata.normalize('NFKD', unicode(properNoun).lower()).encode('ASCII', 'ignore'))
            c.execute('INSERT INTO properNouns(NOUN) values (?)',[name_norm])
        except sqlite3.IntegrityError:
            pass
   
    conn.commit()
    conn.close()



def GetRubish():
    nomeSet = set()
    file = open("rubish.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect("../../../entities.db")     
    c = conn.cursor()       
    c.execute('''CREATE TABLE rubishNames (RUBISH_NAME text primary key)''')
    c.execute('delete from rubishNames')
     
    print "rubishNames"
    print nomeSet
    for name in nomeSet:
        name_norm = unicodedata.normalize('NFKD', unicode(name).lower()).encode('ASCII', 'ignore')
        c.execute('INSERT INTO rubishNames(RUBISH_NAME) values (?)',[name_norm])
    conn.commit()
    conn.close()


def GetCountries():
    nomeSet = set()
    file = open("paises.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect("../../../entities.db")     
    c = conn.cursor()       

    print "countries"
    print nomeSet
    for name in nomeSet:
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'))
        c.execute('INSERT INTO personalities(NAME,NAME_NORM,PRE_REPUTATION,REPUTATION) values (?,?,?,?)',(unicode(name),name_norm,200,0))
    conn.commit()
    conn.close()
    
    
def GetEquiv():
    nomeSet = set()
    file = open("equivalent.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect("../../../entities.db")     
    c = conn.cursor()       

    print "equiv"
    print nomeSet
    for name in nomeSet:
        name_norm = unicode(unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'))
        n = name_norm.split(":")
        c.execute('INSERT INTO nameEquiv(NAME,EQUIV) values (?,?)',(unicode(n[0]),unicode(n[1])))
    conn.commit()
    conn.close()
    
    

GetRubish()
GetNames()
GetCountries()
GetEquiv()