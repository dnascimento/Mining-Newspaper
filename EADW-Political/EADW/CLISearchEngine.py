#!/usr/bin/env python
# -*- coding: utf-8 -*-
from EADW.Analisers.WooshEngine import WooshEngine

# Variables
dbpath = "../storage/news.db"
w = WooshEngine()
w.setDBName(dbpath)
searchWord = ""


print "<Insert q to exit>\n"

while searchWord != "q":
    searchWord = raw_input("#")
    for r in w.searchTopWithEntity(searchWord, 10):
        print "Pontuacao: %.2f" % r[0], "Entidades: "+str(r[2]), "Link:"+str(r[1])