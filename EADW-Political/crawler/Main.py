# -.- coding: utf-8 -.-
from FeedDownloader import FeedDownloader

print "NewsCrawler V8"

dn = FeedDownloader("http://feeds.dn.pt/DN-Politica","feeds.db")
dn.start()

jn = FeedDownloader("http://feeds.jn.pt/JN-Politica","feeds.db")
jn.start()

vg = FeedDownloader("http://economico.sapo.pt/rss/politica","feeds.db")
vg.start()

sol = FeedDownloader("http://sol.sapo.pt/rss/","feeds.db")
sol.start()



