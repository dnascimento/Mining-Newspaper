'''
Created on Mar 25, 2013

@author: darionascimento
'''

import urllib
import re
from bs4 import BeautifulSoup


class newsParser:
        
    def parseSite(self,url):
        fileURL = urllib.urlopen(url)
        
        domain = re.split("http://",url)[1]        
        domain = re.split("\.pt",domain)[0]
        print domain
        
        doc = fileURL.read()        
        soup = BeautifulSoup(doc)
        
        if domain == "expresso.sapo":
            title = soup.select("#artigo")[0].h1.get_text()
            summary = soup.select("#artigo")[0].summary.get_text()
            article =  soup.select("#conteudo")[0].get_text()
                
        if domain == "www.dn":
            title = soup.select("#NewsTitle")[0].get_text()
            summary = soup.select("#NewsSummary")[0].get_text()
            article = soup.select("#Article")[0].get_text()
        
        
        if domain == "www.jn":
             title = soup.select("#NewsTitle")[0].get_text()
             summary = soup.select("#NewsSummary")[0].get_text()
             article = soup.select("#Article")[0].get_text()
        
        
        if domain == "visao.sapo":
             title = soup.select(".article-title")[0].get_text()
             summary = ""
             article = soup.select(".article-body")[0].get_text()
        
        if domain == "sol.sapo":
            title = soup.select("#NewsTitle")[0].get_text()
            summary = ""
            article = soup.select("#NewsSummary")[0].get_text()
        
        
        if domain == "www.rtp":
            title = soup.select("#video_detail")[0].h1.get_text()
            summary = ""
            article =  soup.select("#video_detail")[0].h2.get_text()
        
        print "title:"+title
        print "summary:"+summary 
        print "article:"+article       
        
newsParser().parseSite("http://expresso.sapo.pt/chefe-tiger-bife-do-mar=f729463")