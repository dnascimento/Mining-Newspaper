'''
Created on Mar 9, 2013

Functions to measure the precision, recall and F1 of list of search results.

Input: lista ordenada dos docs e IDs dos relantes


Precision: dos listados, quantos sao relevantes?
Recall: dos relevantes, quantos sao listados?

@author: darionascimento
'''
import math

def irComparison(query,result,goal):
    recall = 0.0
    precision = 0.0
    
    result = set(result)
    goal = set(goal)

    intersection = float(len(result.intersection(goal)))
        
    recall = intersection/len(goal)
    precision = intersection/len(result)
        

    if (precision == 0.0) | (recall == 0.0):
        f = 0
    else:
        f = 2*(precision*recall)/(precision+recall)  


    return {"query": query, "recall": recall, "precision":precision,"f1":f}
   