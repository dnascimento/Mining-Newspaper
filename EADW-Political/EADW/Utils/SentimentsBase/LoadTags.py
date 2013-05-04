'''
Created on May 4, 2013

'''
import os
import unicodedata
import sqlite3

TagFile = "../../sentimentsBase/in/TagFile.txt"
TagDBPath = "../../storage/tags.db"
    
def loadToDB(self):
    
    if os.path.exists(self.TagDBPath):
        os.remove(self.TagDBPath)
    
    # Cria BD nova
    conn = sqlite3.connect(self.TagDBPath)     
    c = conn.cursor()
        
        
    # Carega o ficheiro para a BD
    fd = open(self.TagFile, 'r')
    for line in fd:
        word = line.split(":")[0]
        tag  = line.split(":")[1].split("\n")[0]
        
        if '|' in tag:
            tag = tag.split('|')[0]
            
        # Normalize
        word = unicode(unicodedata.normalize('NFKD', unicode(word).lower()).encode('ASCII', 'ignore'))    
        tag = unicode(tag)
        
        try:
            c.execute('Insert into tags(WORD,TAG) values(?,?)',(word,tag))
        except sqlite3.IntegrityError:
            pass
            
    # Fecha Coneccoes
    conn.commit()
    conn.close() 
    fd.close()