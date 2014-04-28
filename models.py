'''
Created on Jul 22, 2012

@author: paul

This module defines the datastore structure
'''

from google.appengine.ext import db

#Information structure of registered domains' entities
class Domain(db.Model):
    organisation_name = db.StringProperty()
    domain = db.StringProperty()
    
#Information structure of registered sub-domains entities
class SubDomains(db.Model):
    domain = db.StringProperty()
    subdomain = db.StringProperty()

#Event structure       
class Event(db.Model):
    event_title = db.StringProperty()
    target_audience = db.StringProperty()
    event_date = db.StringProperty()
    start_time = db.StringProperty()
    stop_time = db.StringProperty()
    event_venue = db.StringProperty()
    category = db.StringProperty()
    event_domain = db.StringProperty()
    event_description = db.StringProperty()

#Event category   
class Category(db.Model):
    category_domain = db.StringProperty()
    category_name = db.StringProperty()
    category_description = db.StringProperty()
     
#Account Administrators
class Administrators(db.Model):
    emailAddress = db.StringProperty()
    domain = db.StringProperty()
    mobileNumber = db.StringProperty()
    firstName = db.StringProperty()
    secondName = db.StringProperty()
    countryName = db.StringProperty()
    
#Event Subscriptions
class Subscriptions(db.Model):
    emailAddress = db.StringProperty()
    mobileNumber = db.StringProperty()
    category = db.StringProperty()
    subscribed = db.BooleanProperty()