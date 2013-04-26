#!/usr/bin/python
# -*- coding: utf-8 -*-
from WooshEngine import WooshEngine



engine = WooshEngine()
engine.createEmptyIndex()
engine.createIndex("../news.db")
#engine.addLink(u"link1", "Artur", "", " bla bla er sdf df ad Artur <ads asdasd asd asd sss asda sd a")
#engine.addLink(u"link2", "bla", "", " Artur")

print "Search Word? :"
search_word =  raw_input()

for score, link in engine.searchTop(search_word, 5):
    print "Score: "+str(score), "Link: "+link