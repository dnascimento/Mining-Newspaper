'''
Created on Mar 13, 2013

Calcular o pagerank:
usando um dictionary: docID, set_links_to_document

Output: docId, pageRank_value

Input: iterations, dumping_factor

1st: Read the file. 1st entry is docID the rest are the docs which point to him.
2nd: Inverter o graph: Quais os documentos para que este aponta (para doar pontos). 
3rd: Criar um dicionario com:
            Initialize weight with 1/N.
            ID, PesoActual, N_outgoing, linksOutgoing

Para cada ID, dividir PesoActual/N_outgoing e ir somar o peso actual aos que lhe ligam.


-------------------------------------------
Page Rank Algorithm:

    - Each doc entry is initialized with a value v = 1/N
    - Foreach iteration:
        Soma do valor de todas as paginas que apontam para ele (valor/out link)
    
    
    Implementation:
        Initialize v = 1/N, adding this value to dictionary entry. 
        Determine the number of input links
        
        foreach entry:
            Read each input page value, quocient with outlinks and sum to page value
'''

from __future__ import division
import re
from whoosh.index import  open_dir
from whoosh.qparser import  *

class pageRank:
    
    __graph = dict()
    __graphCount = dict()
    __graphRank = dict()
    __NElements = 0
    
    
    def __init__(self,iterations,damping):
        self.__nIterations = iterations
        self.__damping = damping
 
 
 
    def read_file(self):
        f = open("aula04_links.txt")
        
        
        for line in f:
            result = re.split(" ",line[:-1])
            doc = result[0]
            self.__graphRank[doc]= 1
            for w in result[1:]:
                if w == '':
                    continue
                if w not in self.__graph:
                    self.__graph[w] = []
                self.__graph[w].append(doc)
        #print graph
        
        self.__NElements = len(self.__graphRank)
        
        for w in self.__graphRank:
            self.__graphRank[w] = 1/self.__NElements
        
        for doc in self.__graph:
            self.__graphCount[doc] = len(self.__graph[doc])
            
        

    def iteration(self):
        for doc in self.__graph:
            base = self.__graphRank[doc]/self.__graphCount[doc]
            seed = (self.__damping/self.__NElements)+((1-self.__damping)*base)
            
            self.__graphRank[doc] = 0
            for out in self.__graph[doc]:
                self.__graphRank[out] += seed
                


    def sortRank(self):
        sorted_x = sorted(self.__graphRank.iteritems(),key=lambda (k,v): (v,k),reverse = True)
      #  print sorted_x

    def run(self):
        self.read_file()
        for i in range(0,self.__nIterations):     
            self.iteration()
        self.sortRank()
        return self.__graphRank





class searchEngine:
    
    def query(self,queryText):
        queryText = queryText.decode("unicode-escape")

        ix = open_dir("indexdir")
        with ix.searcher() as searcher:
            query = QueryParser("content",ix.schema,group=OrGroup).parse(queryText)
            results = searcher.search(query,limit=100)

        return results

    def rankedQuery(self, queryText,ranking):
        searchResults = self.query(queryText)
        results = dict()
        for i,r in enumerate(searchResults):
                docId = str(searchResults.docnum(i)+1)
                docSeachScore = searchResults.score(i)
                docRank = ranking[docId]
                results[docId] = self.combineReputation(docRank,docSeachScore);
        
        return sorted(results.iteritems(),key=lambda (k,v): (v,k),reverse = True)


    def combineReputation(self,rank,search):
        return rank*0.5+search*0.5



ranking = pageRank(15,0.2).run()
print searchEngine().rankedQuery("How are salivary glycoproteins from CF patients", ranking)


#15 iteracoes fazem o valor convergir
#rank = pageRank(15,0.2)
#rank.run()







        



