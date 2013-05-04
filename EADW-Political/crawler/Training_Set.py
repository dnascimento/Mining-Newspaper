from TAGAnalizer import TAGAnalizer
from collections import Counter
from  ContentDownloader import ContentDownloader
from threading import Thread
import sqlite3, nltk, string, time



class Processor(Thread):

    links = ""
    def set(self,links):
        self.links = links

    def run(self):
        
        global counter
        global lixos
        global tag
        global cntdown
        
        for link in self.links:
            print "->"
            text = cntdown.parseSite(link[0],"",1)
            if text is None:
                continue
            sentences = nltk.sent_tokenize(text.decode("utf8"))
        
            for sentence in sentences:
            
                for c in string.punctuation:
                    sentence = sentence.replace(c,"")
    
                    words = sentence.split(" ")
                
                    for word in words:
        
                        #encontra lixo
                        if(len(word) < 2):
                            lixo.add(word)
                            continue
                        
                        POS = tag.getTagFromBD(word)
                    
                        if  POS == 'NPROP':
                            counter[word] += 1
        print "done"


dbpath = "../news.db"

## Classes
counter = Counter()
toRemovetList= []
cntdown = ContentDownloader("")
tag = TAGAnalizer()

##Inicializar Variaveis
tag.loadToDB()
lixo = set()
ignoreList = set()
links = ""

Threads = 2



#Buscar Links
conn = sqlite3.connect(dbpath)     
cursor = conn.cursor()   
cursor.execute("Select URL from newsStorage")
links = cursor.fetchall()
conn.close()

links = links[:4]

print len(links), " Links Found"

myThreads = []

for i in range(Threads):
    linkN = (len(links)/Threads)
    p = Processor()
    p.set(links[linkN*i:linkN*(i+1)])
    p.start()
    myThreads.append(p)
    
while True:
    
    print "\nThreads in Work ", len(myThreads), "\n"
    
    for p in myThreads:
        if not  p.isAlive():
            myThreads.remove(p)
    if len(myThreads) == 0:
        print "All Returned"
        break
        
    time.sleep(3)
    
print counter.most_common(200), "\n\n"

for name in counter.most_common(200):
    print name
    resp = raw_input("Apagar Nome ?")
    if resp == "y" or resp == "Y":
        toRemovetList.append(name[0])
        
##TODO
IgnoreFile = "../sentimentsBase/in/IgnoreNamesTrainingSet.txt"

fw = open(IgnoreFile, "a")
for word in toRemovetList:
    fw.write(word+":")
fw.flush()
fw.close()

