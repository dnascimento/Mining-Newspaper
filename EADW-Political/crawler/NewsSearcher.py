#!/usr/bin/python
# -*- coding: utf-8 -*-
from WooshEngine import WooshEngine

dbpath = "../news.db"

engine = WooshEngine()
engine.setDBName(dbpath);
#engine.createEmptyIndex()
#engine.createIndex()
#engine.addLink(u"link1", "Artur", "", " bla bla er sdf df ad Artur <ads asdasd asd asd sss asda sd a")
#engine.addLink(u"link2", "bla", "", " Artur")

#print "Search Word? :"
#search_word =  raw_input()
#search_word =  "Artur"


class EADWSearch():

    def searchNews(self,search_word):
        for score, link, entities in engine.searchTopWithEntity(search_word, 5):
            return "Score: "+str(score), "Link: "+link, "Entities: ", entities

     
        