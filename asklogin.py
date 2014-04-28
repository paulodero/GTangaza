from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from landing import LandingPage
from landing import Event
from landing import ViewHandler


webapp.template.register_template_library('tags.filters')

"""The main page handler"""
class MainPage(webapp.RequestHandler):
    
    """Render the main page handler"""
    def get(self):
        user = users.get_current_user()
        
        if user:
            self.redirect('/landing')
        else:
            self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    application = webapp.WSGIApplication([('/',MainPage),
                                          ('/event/.*',Event),
                                          ('/view/.*',ViewHandler),
                                          ('/landing',LandingPage)],debug = True)
    util.run_wsgi_app(application)
if __name__ == "__main__":
    main()
