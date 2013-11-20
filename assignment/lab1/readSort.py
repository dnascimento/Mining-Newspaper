'''
Created on Feb 27, 2013

@author: darionascimento
'''
import quicksort

file = open('numbers','r')

list = []

for line in file:
    line = line[:-1]
    list.append(line)
    
print list
quicksort.quicksort(list,0,len(list))

print list

