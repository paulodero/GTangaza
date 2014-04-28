'''
Created on Jul 19, 2012

@author: paul
'''

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from settings import TEMPLATES_PATH

import ops

DIRECTORY = os.path.dirname(__file__)
_DEBUG = True
values = {}

#Landing Page handler
class LandingPage(webapp.RequestHandler):
  
    #Render the landing page handler
    def get(self):
        category = self.request.get('q',None)
        user = users.get_current_user()
        email = user.email()
        domain = ops.getDomainFromEmail(email)
        isAdministrator = ops.isAdministrator(email)
        if ops.isDomainRegistered(domain):
            values = defaultValues()
            values['isAdministrator']= isAdministrator
            values['events'] = ops.getEvents(domain,category)
            values['categories'] = ops.getCategories()
            values['subscribedCategories'] = ops.getSubscribedCategories(email)
            wireframe = 'events'
            app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
            values['app'] = template.render(app_path, values, debug=_DEBUG)
            path = os.path.join(TEMPLATES_PATH,'page.html')
            self.response.out.write(template.render(path, values, debug=_DEBUG))
        else:
            values = defaultValues()
            path = os.path.join(TEMPLATES_PATH,'signup.html')
            self.response.out.write(template.render(path, values, debug=_DEBUG))

#Help user create event     
class Event(webapp.RequestHandler): 
    def get(self):
        view_info = self.request.path_info.split('/')
        values = defaultValues()
        user = users.get_current_user()
        email = user.email()
        values['categories'] = ops.getCategories()
        values['subscribedCategories'] = ops.getSubscribedCategories(email)
        values['isAdministrator'] = ops.isAdministrator(email)
        values['subdomains'] = ops.getSubdomains(ops.getDomainFromEmail(email))
        
        if len(view_info) < 3:
            return
        
        view = view_info[2]
        if view == 'create_event':
            values['title'] = 'Create an Event'
            wireframe = 'create_event'
        elif view == 'new_category':
            values['title'] = 'Create a new category'
            wireframe = 'new_category'
        app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'page.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))
        
#Render various application views
class ViewHandler(webapp.RequestHandler):
    def get(self):
        view_info = self.request.path_info.split('/')
        values = defaultValues()
        user = users.get_current_user()
        email = user.email()
        domain = ops.getDomainFromEmail(email)
        isAdministrator = ops.isAdministrator(email)
        values['isAdministrator'] = isAdministrator
        values['subdomains'] = ops.getSubdomains(ops.getDomainFromEmail(email))
        if len(view_info)<3:
            return
        view = view_info[2]
        if view == 'events':
            category = self.request.get('q',None)
            wireframe = 'events'
            values['events'] = ops.getEvents(domain,category)
            values['categories'] = ops.getCategories()
            values['subscribedCategories'] = ops.getSubscribedCategories(email)
            values['title'] = 'Events:  %s ' % category
        elif view == 'search_events':
            eventTitle = self.request.get('q',None)
            wireframe = 'events'
            values['events'] = ops.getEventsFromTitle(domain, eventTitle)
            values['categories'] = ops.getCategories()
            values['title'] = 'Event: %s ' % eventTitle
        elif view =='settings':
            values['categories'] = ops.getCategories()
            values['subscribedCategories'] = ops.getSubscribedCategories(email)
            values['title'] = 'Change Settings'
            values['mobileNumber'] = ops.getMobileNumber(email)
            wireframe = 'settings'
        app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'page.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))

def defaultValues():
    user = users.get_current_user()
    nickname = user.nickname()
    logout_url = users.create_logout_url('/')
    return  {
                            'owner': user.email(),
                            'nickname': nickname,
                            'logout_url': logout_url,
              }      