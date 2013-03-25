# -.- coding: utf-8 -.-
from FeedDownloader import FeedDownloader

dn = FeedDownloader("http://feeds.dn.pt/DN-Politica", "DN-Politica")
dn.start()

jn = FeedDownloader("http://feeds.jn.pt/JN-Politica", "JN-Politica")
jn.start()

vg = FeedDownloader("http://visao.sapo.pt/static/rss/visao-geral.xml", "Visao-Geral")
vg.start()

sol = FeedDownloader("http://sol.sapo.pt/rss/", "Sol")
sol.start()



