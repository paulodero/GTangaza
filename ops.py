'''
Created on Jul 22, 2012

@author: paul

This module contains functions defined in the application
'''
import models
from google.appengine.api import mail
from smsSender import NexmoMessage

#Functions to get data from the datastore
#A function to get details of a particular sub-domain sub-domain
def getSubdomain(subdomain):
    q = models.SubDomains().all().filter('subdomain =', subdomain)
    row = q.fetch(1)
    return row

#Get sub-domains
def getSubdomains(domain):
    q = models.SubDomains().all().filter('domain =', domain)
    row = q.fetch(10)
    return row

#Find out if the domain is registered
def isDomainRegistered(domain):
    q = models.SubDomains().all().filter('subdomain =', domain)
    row = q.fetch(1)
    if row:
        return True
    else:
        return False
#Find out if the user is an administrator
def isAdministrator(email):
    q = models.Administrators().all().filter('emailAddress =', email)
    row = q.fetch(1)
    if row:
        return True
    else:
        return False
     
#A function to get sub-domain from an email address
def getDomainFromEmail(email):
    emailarr = email.split('@')
    subdomain = emailarr[1]
    return subdomain

#Get most recent events
def getEvents(domain,category):
    if category == 'all' or category == None:
        q = models.Event().all().filter('event_domain =', domain)
    else:
        q = models.Event().all().filter('category =', category)
    rows = q.fetch(10)
    return rows

def getEventsFromTitle(domain,eventTitle):
    q = models.Event().all().filter('event_domain =', domain).filter('event_title =', eventTitle)
    rows = q.fetch(10)
    return rows

#Get categories
def getCategories():
    q = models.Category().all()
    rows = q.fetch(10)
    return rows

#Get subscribed categories
def getSubscribedCategories(emailAddress):
    q = models.Subscriptions().all().filter('emailAddress =', emailAddress).filter('subscribed =', True)
    rows = q.fetch(10)
    return rows

#Get Subscribers' Emails
def getSubscribersEmails(category):
    q = models.Subscriptions().all().filter('category =', category)
    rows = q.fetch(10)
    return rows

#Get Mobile Number
def getMobileNumber(email):
    q = models.Administrators().all().filter('emailAddress =', email)
    rows = q.fetch(1)
    for row in rows:
        return row.mobileNumber
#Functions to add data into datastore 

#Remove subdomain
def removeSubdomain(subdomain):
    q = models.SubDomains().all().filter('subdomain =', subdomain)
    rows = q.fetch(1)
    for row in rows:
        row.domain = None
        row.put()  
#Add a new event
def addEvent(eventTitle,targetAudience,eventDate,startTime,
             stopTime,eventVenue,category,eventDomain,eventDescription):
    row = models.Event()
    row.event_title = eventTitle
    row.target_audience = targetAudience
    row.event_date = eventDate
    row.start_time = startTime
    row.stop_time = stopTime
    row.event_venue = eventVenue
    row.category = category
    row.event_domain = eventDomain
    row.event_description = eventDescription   
    row.put()

#Add domain
def addDomain(organization_name,domain):
    key = domain
    row = models.Domain(key_name = key)
    row.organisation_name = organization_name
    row.domain = domain
    row.put()
    
#Add subdomain
def addSubdomain(organization_name,domain):
    key = domain
    row = models.SubDomains(key_name = key)
    row.domain = domain
    row.SubdomainName = organization_name
    row.subdomain = domain
    row.put()

#Add subdomain given admin Email
def addSubdomainFromEmail(email,subdomain):
    q = models.Administrators().all().filter('emailAddress =', email).fetch(1)
    
    for row in q:
        domain = row.domain
    key = subdomain
    row = models.SubDomains(key_name = key)
    row.domain = domain
    row .subdomain = subdomain
    row.put()
         
#Add a new category
def addCategory(domain,category_name,category_description):
    key = removeSpacesInString(category_name)
    row = models.Category(key_name = key)
    row.category_domain = domain
    row.category_name = category_name
    row.category_description = category_description
    
    row.put()

#Add mobile number
def addMobileNumber(emailAddress,mobileNumber):
    rows = models.Subscriptions().all().filter('emailAddress =', emailAddress)
    for row in rows:
        row.mobileNumber = mobileNumber
        row.put()
    q = models.Administrators().all().filter('emailAddress =', emailAddress)
    
    for value in q:
        value.mobileNumber = mobileNumber
        value.put()
               
#Utility functions
#NotifySubscribers
def NotifySubscribers(category,eventTitle,startTime,stopTime,eventDate,eventVenue):
    subscribersEmail = getSubscribersEmails(category)
    data_in_html = '<html><body>%s, %s, %s</body></html>' % (eventTitle,startTime,stopTime)
    message = 'There will be %s on %s at %s starting from %s to %s' % (eventTitle,eventDate,eventVenue,startTime,stopTime)
    for subscriber in subscribersEmail:
        sender = 'paulodero@students.jkuat.ac.ke'
        to = subscriber.emailAddress
        subject = 'GTangaza Alert System'
        sendMail(sender,to,subject,data_in_html)
        sendSms(subscriber.mobileNumber, message)
    
#Send mail function
def sendMail(sender,to,subject,body):
    message = mail.EmailMessage(sender=sender,subject = subject)
    message.to = 'Subscriber <%s>' % to
    message.html = """ %s """ % (body)
    message.Send()

#Send sms
def sendSms(to,message):
    r = "json"
    u = "1aa428a2"
    p = "eed11fe1"
    f = "marcuz"
    t = to
    m = message
        
    msg = {'reqtype': r, 'password': p, 'from': f, 'to': t, 'username': u}
    
    # text message
    msg['text'] = m
    sms = NexmoMessage(msg)
    m += " GTangaza"
    sms.set_text_info(m)
    sms.send_request()
       
#Remove spaces between strings
def removeSpacesInString(thestrings):
    thestringsarr = thestrings.split(' ')
    string = ''
    for thestring in thestringsarr:
        string += thestring
    return string

#Subscribe for updates
def addSubscription(category,emailAddress):
    key = '%s_%s' % (category,emailAddress)
    row = models.Subscriptions(key_name = key)
    row.category = category
    row.emailAddress = emailAddress
    row.subscribed = True
    row.put()
    
def unsubscribe(category, emailAddress):
    key = '%s_%s' % (category,emailAddress)
    row = models.Subscriptions(key_name = key)
    row.category = category
    row.emailAddress = emailAddress
    row.subscribed = False
    row.put()
    
#GTangaza Account sign up
def signUp(emailAddress,domain,mobileNumber,firstName,secondName,countryName):
    key = domain
    row = models.Administrators(key_name = key)
    row.emailAddress = emailAddress
    row.domain = domain
    row.mobileNumber = mobileNumber
    row.firstName = firstName
    row.secondName = secondName
    row.countryName = countryName
    row.put()
