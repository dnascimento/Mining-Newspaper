#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 3, 2013
'''

from bottle import route, run, template

import bottle
from bottle import route, run
from bottle import static_file 
from bottle import response
from json import dumps


@route('/', method='GET')
def homepage():
    return static_file('index.php', root='./webPage/')

@route('/favicon.ico', method='GET')
def favicon():
    return static_file('favicon.ico', root='./webPage/')

@route('/search/:id', method='GET')
def get_event(id):
    #return "dario"
    #return NewsSearcher.EADWSearch().searchNews("dario")
    response.content_type = 'application/json'    
    result = []
    result.append(dict(title = 'SITE DO IST',summary="Isto e o sumario do site",entities="dario,andre,carlos"))
    result.append(dict(title = 'SITE DO IST',summary="Isto e o sumario do site",entities="dario,andre,carlos"))
    return dumps(result)

@route('/static/')
def send_static():
    return static_file('index.php', root='./webPage/')

@route('/static/<path:path>')
def send_static(path):
    return static_file(path, root='./webPage/')
   
bottle.debug(True) 
run(host='172.20.81.172', port=8080)