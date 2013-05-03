'''
Created on May 3, 2013
'''

from bottle import route, run, template

import bottle
from bottle import route, run
import NewsSearcher

print NewsSearcher.EADWSearch().searchNews("COELHO")

@route('/', method='GET')
def homepage():
    return 'Hello world!'
    
@route('/search/:id', method='GET')
def get_event(id):
    #return "dario"
    #return NewsSearcher.EADWSearch().searchNews("dario")
    return dict(name = 'Event ' + str(id))

@error(404)
def error_route(code):
    redirect('/index')
   
bottle.debug(True) 
run(host='194.210.221.72', port=8080)