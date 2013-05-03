

#ADJ(ective), N(oun), V(erb) and IDIOM), and
#Polarity (POL), which can be positive (1), negative (-1) or neutral (0);
#Some entries also include an additional code (REV), which refers to specific notes included by the annotator. At this point, we can find the following notations:



fileName = "/home/artur-adm/teste/SentiLex-flex-PT03.txt"
#fileName = "/home/artur-adm/teste/SentiLex-flex-PT03.txt"


neglist = []
poslist = []

lex = open(fileName, "r")
for line in lex:
    #print line
#    palavras = line.split('.')[0].split(',')
#    pos = line.split('Po')[1].split('=')[1].split(';')[0]
#    polarity = int(line.split('POL:N')[1].split('=')[1].split(';')[0])
    
    #print len(palavras),
    #    print line
    
    #print pos, polarity, palavras

#    if(polarity > 0):
#        poslist.append(palavras[0])
#        poslist.append(palavras[1])
#    else:
#        neglist.append(palavras[0])
#        neglist.append(palavras[1])
        
#print "Pos", poslist
#print "Neg", list(negative)[:100]


f = open("negative.txt", 'w')
for word in neglist:
    f.write(word+":")
    
f = open("positive.txt", 'w')
for word in poslist:
    f.write(word+":")