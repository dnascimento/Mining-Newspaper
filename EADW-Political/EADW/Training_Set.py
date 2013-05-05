#!/usr/bin/env python
# -*- coding: utf-8 -*-
from EADW.Analisers.TAGAnalizer import TAGAnalizer
from collections import Counter
from EADW.Downloaders.ContentDownloader import ContentDownloader
from threading import Thread
import sqlite3, nltk, string, time, re, unicodedata, os, hashlib
from nltk.downloader import download

class LinkDowloader(Thread):

    path = "../storage/tmpArticle/"
    salt = ""
    links = ""
    def set(self,links,salt):
        self.links = links
        self.salt = salt
            
    def run(self):
        global cntdown
        global Nnoticias
        for link in self.links:
            if not os.path.exists(self.path+hashlib.sha1(link[0]).hexdigest()+"Article.txt"):
                text = cntdown.parseSite(link[0],"",1)
                if text is None:
                    continue
                f = open(self.path+hashlib.sha1(link[0]).hexdigest()+"Article.txt", "w+")
                f.write(text)
                f.flush()
                f.close()
            Nnoticias += 1

# Classe que cada Thread Executa
class Processor(Thread):

    links = ""
    path = "../storage/tmp/"
    def set(self,links):
        self.links = links

    def strip_punctuation(self,text):
        punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
        return ''.join(x for x in text if unicodedata.category(x) not in punctutation_cats)
    
    def run(self):
        
        global counter
        global lixo
        global tag
        global cntdown
        global Nnoticias
        global downloaded
        
        for link in self.links:
            if not os.path.exists(self.path+hashlib.sha1(link[0]).hexdigest()+"Article.txt"):
                continue
            
            f = open(self.path+hashlib.sha1(link[0]).hexdigest()+"Article.txt", "r")
            text = f.read()
            f.close()
            
            #text = cntdown.parseSite(link[0],"",1)
            if text is None:
                continue
            sentences = nltk.sent_tokenize(text.decode("utf8"))
            Nnoticias += 1
            for sentence in sentences:
                #re.sub(ur"\p{P}+ \„\“\‘", " ", sentence)
                sentence = self.strip_punctuation(sentence)
                words = sentence.split(" ")
                for word in words:
                    
                    
                    
                    #encontra lixo
                    if(len(word) < 2):
                        continue
                    
                    #So Aceita palavras com letra Grande
                    if not word[0].isupper():
						continue
					
                    #Ignora Processados
                    if word in ignoreList or word in filteredNames:
                        continue

                    POS = tag.getTagFromBD(word)
                    if  POS == 'NPROP' :
                        counter[word] += 1
        




dbpath = "../storage/news.db"
IgnoreFile = "Utils/SentimentsBase/in/IgnoreNamesTrainingSet.txt"
Filtred = "Utils/SentimentsBase/in/GoodNamesTrainingSet.txt"

## Classes
counter = Counter()
downloaded = 0
toRemovetList= []
cntdown = ContentDownloader("")
tag = TAGAnalizer()

##Inicializar Variaveis
tag.loadToDB()
lixo = set()
ignoreList = set()
links = ""
Threads = 10
Nnoticias = 0
newProcessedNames = []

# Ler os Filtros
f = open(Filtred, "r+")
fw = open(IgnoreFile, "r+")

ignoreList = fw.read().split(":")
fw.close()

filteredNames = f.read().split(":")
f.close()



#Buscar Links
conn = sqlite3.connect(dbpath)     
cursor = conn.cursor()   
cursor.execute("Select URL from newsStorage")
links = cursor.fetchall()
conn.close()

print len(links), " Links Found"

#links = links[2000:]
Nnoticias = 0

print len(links), " Links to Be Processed"

myDonwloadThreads = []
Dthreads = 10
for i in range(Dthreads):
    linkN = (len(links)/Threads)
    d = LinkDowloader()
    d.set(links[linkN*i:linkN*(i+1)],i)
    d.start()
    myDonwloadThreads.append(d)

while True:
    
    print len(myDonwloadThreads), " Threads in Work ", Nnoticias, " Descaregadas"
    
    for d in myDonwloadThreads:
        if not  d.isAlive():
            myDonwloadThreads.remove(d)
    if len(myDonwloadThreads) == 0:
        print "All Returned"
        break
        
    time.sleep(10)


#os._exit(1)

print "\n PROCESSING \n"
Nnoticias = 0
myThreads = []

for i in range(Threads):
    linkN = (len(links)/Threads)
    p = Processor()
    p.set(links[linkN*i:linkN*(i+1)])
    p.start()
    myThreads.append(p)
    
while True:
    
    print len(myThreads), " Threads in Work ", Nnoticias, "Processed ",  len(counter), "new Words Found"
    
    for p in myThreads:
        if not  p.isAlive():
            myThreads.remove(p)
    if len(myThreads) == 0:
        print "All Returned"
        break
        
    time.sleep(10)
    
print counter.most_common(150), "\n\n"

#print "Ignoring:", ignoreList
names = len(counter.most_common(150))
## Pregunta ao utilizador se e um nome proprio
for name in counter.most_common(150):
    
    #Ignora ficheiros ja analizados
    if name[0] in ignoreList or name[0] in filteredNames:
        continue
    
    print "Apagar Nome [", name[0].decode("utf8"), "] faltam", names
    names -= 1
    resp = raw_input()
    
    if resp == "y" or resp == "Y":
        toRemovetList.append(name[0])
    else:
        newProcessedNames.append(name[0])
        
##TODO

fw = open(IgnoreFile, "a+")
for word in toRemovetList:
    fw.write(word+":")
fw.flush()
fw.close()

f = open(Filtred, "a+")
for word in newProcessedNames:
    f.write(word+":")
f.flush()
f.close()

print "DONE"







