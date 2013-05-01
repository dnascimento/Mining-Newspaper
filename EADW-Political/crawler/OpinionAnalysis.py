'''
Created on Mar 25, 2013

1 Load the feed from feedURL and save it on SQLite DB
2 The SQLite Schema doesnt allow to save the same url
'''




class OpinionAnalysis(Thread):         
    
    def __init__(self, entitiesList,wordsTree):
        self.__entitiesList = entitiesList;
        self.__wordsTree = wordsTree;
        
    def ProcessOpinion(self,EntitiesList,WordsTree):
        print "TODO"