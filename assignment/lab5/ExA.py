'''
Created on Apr 3, 2013

Por regressao linear para descobrir os weight de uma mastriz
@author: darionascimento
'''


import numpy as np
from numpy import linalg


#Cada X e uma linha

X = [(0,3), (2,3), (2.5,3.6), (4,4.8)]
y = [7.3, 8.6, 8.5, 9.0]
w = lregression(X,y)
print w



def lregression(X,y):
    l = len(y)
    
    #Converter  X num array com:
    #x1 x2 x3 x4
    #1  1  1  1
    #Inverter o array de row para column
    A = np.vstack([np.array(X).T,np.ones(1)])
    
    #Resolve a matriz e devolve os pesos minimos
    return linalg.lstsq(A.T,y)[0]