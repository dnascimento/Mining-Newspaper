#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from whoosh.index import create_in
from whoosh.fields import Schema, NUMERIC, TEXT

dbName = "feeds.db"
conn = sqlite3.connect(dbName)



c = conn.cursor()
c.execute('''SELECT * FROM feedsCrawling''')
feeds = c.fetchall()
print len(feeds)


print "Search Word? :"
search_word =  raw_input()