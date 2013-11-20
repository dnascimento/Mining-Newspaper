'''
Created on Mar 9, 2013

@author: darionascimento
'''

from whoosh.index import open_dir
from whoosh.qparser import  *
#from whoosh.scoring import Cosine


def searchEADW(text):
    text = text.decode("unicode-escape")
    ix = open_dir("indexdir")

    #with statment allow to close automatically the file
    #"content" as default searching field in ix schema 
    #parse define a query que vamos fazer
    
    #with ix.searcher(weighting=whoosh.scoring.Cosine()) as searcher:

    with ix.searcher() as searcher:
        query = QueryParser("content",ix.schema,group=OrGroup).parse(text)
        results = searcher.search(query,limit=100)
        result = sorted(results.docs())
        
    return result








