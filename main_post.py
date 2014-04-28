'''
Created on Oct 1, 2012

@author: paul

Main module to post data into the datastore
'''
import ops
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users

DIRECTORY = os.path.dirname(__file__)
_DEBUG = True

class PostHandler(webapp.RequestHandler):
    def get(self):
        eventTitle = self.request.get('event_title', None)
        targetAudience = self.request.get('target_audience', None)
        eventDate = self.request.get('event_date', None)
        startTime = self.request.get('start_time', None)
        stopTime = self.request.get('stop_time', None)
        eventVenue = self.request.get('event_venue', None)
        category = self.request.get('category', None)
        eventDomain = self.request.get('event_domain', None)
        eventDescription = self.request.get('event_description', None)
        ops.addEvent(eventTitle, targetAudience, eventDate, startTime, stopTime, eventVenue, category, eventDomain, eventDescription)
        ops.NotifySubscribers(category, eventTitle, startTime, stopTime,eventDate,eventVenue)
        self.redirect('/landing')
        
class PostCategoryHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        emailAddress = user.email()
        domain = ops.getDomainFromEmail(emailAddress)
        category_name = self.request.get('category_name',None)
        category_description = self.request.get('category_description',None)
        ops.addCategory(domain,category_name, category_description)
        self.redirect('/')
        
class SettingsHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        emailAddress = user.email()
        mobileNumber = self.request.get('mobileNumber',None)
        ops.addMobileNumber(emailAddress,mobileNumber)
        self.redirect('/')

#Subscribe to a category       
class SubscriptionHandler(webapp.RequestHandler):
    def get(self):
        category = self.request.get('category',None)
        emailAddress = self.request.get('email',None)
        ops.addSubscription(category,emailAddress)
        self.redirect('/',)
        
#Unsubscribe from a category
class UnsubscribeHandler(webapp.RequestHandler):
    def get(self):
        category = self.request.get('category', None)
        emailAddress = self.request.get('email', None)
        ops.unsubscribe(category,emailAddress)
        self.redirect('/')
        
#Handles the sign up process
class SignupHandler(webapp.RequestHandler):
    def get(self):
        mobileNumber = self.request.get('mobileNumber', None)
        firstName = self.request.get('firstName', None)
        secondName = self.request.get('lastName', None)
        countryName = self.request.get('countryName', None)
        orgName = self.request.get('orgName', None)
        user = users.get_current_user()
        emailAddress = user.email()
        domain = ops.getDomainFromEmail(emailAddress)
        ops.signUp(emailAddress,domain,mobileNumber,firstName,secondName,countryName)
        ops.addDomain(orgName, domain)
        ops.addSubdomain(orgName,domain)
        self.redirect('/',)
        
#Adding a subdomain
class PostSubDomainHandler(webapp.RequestHandler):
    def get(self):
        subdomain = self.request.get('subdomain', None)
        user = users.get_current_user()
        email = user.email()
        ops.addSubdomainFromEmail(email,subdomain)
        self.redirect('/view/settings')

#Remove subdomain
class RemoveSubDomainHandler(webapp.RequestHandler):
    def get(self):
        subdomain = self.request.get('q', None)
        ops.removeSubdomain(subdomain)
        self.redirect('/view/settings') 
def main():
    application = webapp.WSGIApplication(
      [
        ('/post', PostHandler),
        ('/subscription', SubscriptionHandler),
        ('/unsubscribe', UnsubscribeHandler),
        ('/new_category', PostCategoryHandler),
        ('/settings', SettingsHandler),
        ('/signup', SignupHandler),
        ('/addsubdomain', PostSubDomainHandler),
        ('/remove_subdomain', RemoveSubDomainHandler)
      ],
      debug=_DEBUG)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
