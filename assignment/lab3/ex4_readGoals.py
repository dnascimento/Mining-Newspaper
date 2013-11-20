'''
Created on Mar 9, 2013

@author: darionascimento
'''
import re
from ex2_query import searchEADW
from ex3_analysis import irComparison

file = open("aula03_queries.txt")

table = []
statistics = {"recall": 0, "precision":0,"f1":0,"total":0}
while True:
    query = file.readline()
    query = query.rstrip('\n')
    if query == "":
        break
    
    ids = file.readline()
    ids = ids.rstrip(' \n')
    goalText = re.split("\D",ids)
    
    
    goal = []
    for dat in goalText:
        if(dat != ''):
            goal.append(int(dat))
        
    result = searchEADW(query)
    stats = (irComparison(query, result, goal))
    statistics["recall"] += stats["recall"]
    statistics["precision"] += stats["precision"]
    statistics["f1"] += stats["f1"]
    statistics["total"] += 1.0
    table.append(stats)
   
    

print table
 
statistics["recall"] = float(statistics["recall"]/statistics["total"])
statistics["precision"] = statistics["precision"]/statistics["total"]
statistics["f1"] = statistics["f1"]/statistics["total"]

print statistics