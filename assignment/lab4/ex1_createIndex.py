'''
Created on Mar 9, 2013

@author: darionascimento

Whosh is an indexing and searchng libray.
http://pythonhosted.org/Whoosh/
'''
import os
from whoosh.index import create_in
from whoosh.fields import *


'''
To begin using Whoosh, you need an index object. The first time you create an index you mush define the index's schema 
The shema lists the fields in the index.
Field can be indexed: can be searched 
Or can be stored (the value that thets indexed is returned with the results.
fields can be: ID, STORED, KEYWORD, TEXT, NUMERIC, BOOLEAN, DATETIME
'''

#This schema has two fields: id and content
schema = Schema(id = NUMERIC(stored=True), content=TEXT)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    
#This creates a storage object to contain the index    
ix = create_in("indexdir",schema)

#Add documents to index
writer = ix.writer()


#Document interation
#Open file
file = open("aula03_cfc.txt")

for line in file:
    #Regex: First 5 numbers are the ID, rest content
    idText = line[0:5]
    contentText = line[5:]
    contentText = contentText.decode("unicode-escape")
    writer.add_document(id=idText,content=contentText)

writer.commit()

print "Index Created"


