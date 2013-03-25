'''
Created on Mar 25, 2013

@author: darionascimento
'''

import feedparser

d = feedparser.parse("https://news.google.pt/news/feeds?pz=1&cf=all&ned=pt-PT_pt&hl=pt-PT&q=Politica&output=rss")
d['feed']['title']