'''
Created on Mar 25, 2013
'''
import re
from collections import Counter


def GetNames():
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
                list.append((unicode(name),int(value)))
            except ValueError:
                pass
        else:
            name = word
        i += 1
    
    return sorted(list,key=lambda entry: entry[0])
