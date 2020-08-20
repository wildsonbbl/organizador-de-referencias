#!/usr/bin/env python
# coding: utf-8

# In[1]:


try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

import re
import sqlite3


# In[2]:


conn = sqlite3.connect('referencias.sqlite')
cur = conn.cursor()


# In[3]:


cur.executescript('''
DROP TABLE IF EXISTS referencias;
DROP TABLE IF EXISTS titulos;
DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS referencias ( 
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    referencia TEXT UNIQUE
    );
CREATE TABLE IF NOT EXISTS titulos ( 
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    titulo TEXT,
    referencia_id INTEGER
    );
CREATE TABLE IF NOT EXISTS urls ( 
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    url TEXT, 
    titulo_id INTEGER 
    );
    ''')


# In[4]:


fhand = open('referencias para corrigir.txt','r')
line = ''
for text in fhand:
    words = text.split()
    for word in words:
        if not re.search("^\d+\.", word):
            line = line + " " + word
        else:
            line = line + " " + word
            line = line.strip()
            cur.execute('''INSERT OR IGNORE INTO referencias (referencia) VALUES ( ? )''', ( line, ) )
            cur.execute('SELECT id from referencias WHERE referencia = ?', ( line,))
            referencia_id = cur.fetchone()[0]
            title = re.findall('[A-Z]\.\s([A-Z][a-zA-Z]{2,}.+?),', line)
            if title == []: 
                title = [line,]
            cur.execute('INSERT OR IGNORE INTO titulos ( titulo, referencia_id ) VALUES ( ?, ? )', ( title[0], referencia_id ) )
            cur.execute('SELECT id from titulos WHERE  titulo = ?', ( title[0], ))
            titulo_id = cur.fetchone()[0]
            for url in search(title[0], tld="com", num=1, stop=1, pause=2):
                cur.execute('INSERT OR IGNORE INTO urls ( url, titulo_id ) VALUES( ?, ? )', ( url, titulo_id))
            line = ''
conn.commit()


# In[5]:


refhand = cur.execute('''
    SELECT referencia, titulo, url 
    from urls JOIN titulos JOIN referencias 
    on referencias.id = titulos.referencia_id AND titulos.id = urls.titulo_id
    ''')
for referencia, titulo, url in refhand:
    print(referencia)
    print(titulo)
    print(url + '\n')
    


# In[ ]:




