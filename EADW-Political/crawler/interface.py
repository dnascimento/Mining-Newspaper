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
    return NewsSearcher.EADWSearch().searchNews("dario")
    #return dict(name = 'Event ' + str(id))
   
bottle.debug(True) 
run(host='localhost', port=8888)