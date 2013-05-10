
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 3, 2013
'''
import urllib2
from bottle import route, run, template

import socket
import bottle
from bottle import route, run
from bottle import static_file 
from bottle import response
from json import dumps
import CommandInterface


@route('/', method='GET')
def homepage():
    return bottle.redirect('/static/')

@route('/favicon.ico', method='GET')
def favicon():
    return static_file('favicon.ico', root='./webPage/')

@route('/entity/<path:path>', method='GET')
def get_entity(path):
    response.content_type = 'application/json'
    path = path.decode('utf-8')
    result = CommandInterface.getEntityDetails(path)
    print  dumps(result)
    return dumps(result)
    


@route('/search/:id', method='GET')
def get_event(id):
    response.content_type = 'application/json'    
    result = CommandInterface.searchNews(id)
    return dumps(result)

@route('/partidosPositive/',method="GET")
def partidosPositive():
    response.content_type = 'application/json'    
    result = CommandInterface.partidosPositive()
    return dumps(result)

@route('/partidosNeutral/',method="GET")
def partidosNeutral():
    response.content_type = 'application/json'    
    result = CommandInterface.partidosNeutral()
    return dumps(result)

@route('/partidosNegative/',method="GET")
def partidosNegative():
    response.content_type = 'application/json'    
    result = CommandInterface.partidosNegative()
    return dumps(result)

@route('/partidosOpinion/',method="GET")
def partidosOpinion():
    response.content_type = 'application/json'    
    result = CommandInterface.partidosOpinion()
    return dumps(result)

@route('/topWords/',method="GET")
def getWords():
    response.content_type = 'application/json'    
    result = CommandInterface.topWords()
    return dumps(result)

@route('/topCountries/',method="GET")
def getCountries():
    response.content_type = 'application/json'    
    result = CommandInterface.topCountries()
    return dumps(result)

@route('/static/')
def send_static():
    return static_file('index.php', root='./webPage/')

@route('/static/<path:path>')
def send_staticPath(path):
    return static_file(path, root='./webPage/')
   
bottle.debug(True) 
#my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
#Tentar com IP Publico
#try:
#    run(host=my_ip, port=8080)
#except socket.error:
#    run(host="localhost", port=8080)

run(host="0.0.0.0", port=8080)
