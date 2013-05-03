'''
Created on May 3, 2013
'''
import re

file = open('SentiLex-flex-PT03.txt')

out = open("lexicon.txt","w+")

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
            if len(opinions) == 0:
                result = sentence+":"+POS+":"+":"+Sex
            else:
                result = sentence+":"+POS+":"+opinions[i].split("=")[1]+":"+Sex
                if i < (len(opinions) - 1):
                    i += 1
                    
            print result
            out.write(result+"\n")
            
out.close()
file.close()       
