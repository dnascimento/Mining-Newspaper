'''
Created on Mar 25, 2013
'''
import re
from collections import Counter
import sqlite3

#
#Extracts a name:reputation list and a  nomial names list
#
def GetNames():
    nomeSet = set()
    file = open("personalities.txt")
    line = file.readline()
    list = []
    words = re.split('"',line)
    i = 0
    name = ""
    for word in words:
        if i%2== 0:
            value = word[1:-1]
            try:
                nome = unicode(name)
                for nomePart in nome.split(" "):
                    if nomePart != '' :
                        nomeSet.add(nomePart)
                    
                list.append((nome,int(value)))
            except ValueError:
                pass
        else:
            name = word
        i += 1
    
    a = sorted(list,key=lambda entry: entry[0])
    
        
    conn = sqlite3.connect("entities.db")     
    c = conn.cursor()       
    c.execute('''CREATE TABLE personalities (NAME text primary key, PRE_REPUTATION INTEGER, REPUTATION INTEGER)''')
    c.execute('delete from personalities')
    c.execute('''CREATE TABLE properNouns (NOUN text primary key)''')
    c.execute('delete from properNouns')
     
    for pair in a:
        c.execute('INSERT INTO personalities(NAME,PRE_REPUTATION,REPUTATION) values (?,?,?)',(unicode(pair[0]),pair[1],0))
    
    print nomeSet
    for properNoun in nomeSet:
        try:
            c.execute('INSERT INTO properNouns(NOUN) values (?)',[unicode(properNoun).lower()])
        except sqlite3.IntegrityError:
            pass
   
    conn.commit()
    conn.close()



def GetRubish():
    nomeSet = set()
    file = open("rubish.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect("entities.db")     
    c = conn.cursor()       
    c.execute('''CREATE TABLE rubishNames (RUBISH_NAME text primary key)''')
    c.execute('delete from rubishNames')
     
    print nomeSet
    for name in nomeSet:
        c.execute('INSERT INTO rubishNames(RUBISH_NAME) values (?)',[unicode(name).lower()])
    conn.commit()
    conn.close()


def GetCountries():
    nomeSet = set()
    file = open("paises.txt")
    for line in file:
        nomeSet.add(unicode(line[:-1]))
            
    conn = sqlite3.connect("entities.db")     
    c = conn.cursor()       

    print nomeSet
    for name in nomeSet:
        c.execute('INSERT INTO personalities(NAME,PRE_REPUTATION,REPUTATION) values (?,?,?)',(unicode(name),200,0))
    conn.commit()
    conn.close()

GetRubish()
GetNames()
GetCountries()