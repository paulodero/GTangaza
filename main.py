'''
Created on Sep 25, 2012

@author: paul

This is the main module for the application
'''
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

DIRECTORY = os.path.dirname(__file__)
_DEBUG = True

class MainHandler(webapp.RequestHandler):    
    def self(self):
        values = defaultValues()
        wireframe = 'events'
        app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(DIRECTORY, os.path.join('templates', 'page.html'))
        self.response.out.write(template.render(path, values, debug=_DEBUG))
    
class ViewHandler(webapp.RequestHandler):
    def self(self):
        view_info = self.request.path_info.split('/')

        if len(view_info) < 3:
            return
        
        view = view_info[2]
        values = defaultValues()
        
        values['current_view'] = view
        wireframe = 'help'
        
        if view == 'create_event':
            wireframe = 'create_event'
            values['title'] = 'Create an Event'
        app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(DIRECTORY, os.path.join('templates', 'page.html'))
        self.response.out.write(template.render(path, values, debug=_DEBUG))
def defaultValues():
    return {
            }
    
def main():
    application = webapp.WSGIApplication([
        ('/view/.*',MainHandler)],
        debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

