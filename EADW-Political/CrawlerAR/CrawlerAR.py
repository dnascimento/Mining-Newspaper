'''
Created on May 3, 2013
'''


from bs4 import BeautifulSoup
import unicodedata
import codecs

file = codecs.open("deputados.html","r")
doc = str(file.readlines())   
soup = BeautifulSoup(doc)

print "download"

#os a com href que contem biografia
def cond(x):
    if x:
        return str(x).find("Biografia") != -1
    else:
        return False
    
listaDeputados = []
rows = soup.findAll('a', {'href': cond})

out = open("out.txt","w+")

for entry in rows:
    entry = entry.text.decode('string-escape').decode("utf-8")
    listaDeputados.append((entry));
    out.write(entry+"\n")
    
#sacar partido
#CDS-PP PS PSD PCP BE PEV
#os a com href que contem biografia

def cond(x):
    if x:
        return str(x).find("Biografia") != -1
    else:
        return False

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
result = {}
for link in rows:
    link = link.text
    if isPartido(link):
        result[listaDeputados[i]] = link
        i += 1
    

print result

    
    
    
    
out.close()
out = open("out.txt","r") 
#print out.readlines()   
#print listaDeputados