import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        me =  users.get_current_user()
        print "hi"
        print me
        start_template = jinja_env.get_template("templates/main.html")
        jinja_values = {}

        if not me:
            jinja_values["signin_page_url"] = users.create_login_url('/')
        else:
            jinja_values["signout_page_url"] = users.create_logout_url('/')
        print jinja_values

        self.response.write(start_template.render(jinja_values))

class MainHandler (webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('main.html')
        self.response.write(main_template.render())

class MusicHandler (webapp2.RequestHandler):
    def get(self):
        music_template = jinja_env.get_template('templates/music.html')
        self.response.write(music_template.render())

class GifsHandler (webapp2.RequestHandler):
    def get(self):
        search_term = self.request.get('search')
        if search_term:
            updateSearchCount(search_term)
        else:
            search_term = "satisfying"
        params = {'api_key': 'F3eg1VxjOgwzWvn4J49lhRAFXBBh6Z0Z', #api key is from giphy.com
                'q': search_term,
                'rating': 'g',
                'limit': 50}
        form_data = urllib.urlencode(params)
        api_url = 'http://api.giphy.com/v1/gifs/search?' + form_data

        response = urllib2.urlopen(api_url)
        content = json.loads(response.read())

        gif_urls = []
        for img in content['data']:
            url = img['images']['original']['url']
            gif_urls.append(url)

        template = jinja_env.get_template('templates/gifs.html')
        variables = {'gif_urls': gif_urls,
                    'q': search_term}
        self.response.write(template.render(variables))

    # gifs_template = jinja_env.get_template('gifs.html')
    # self.response.write(gifs_template.render())

class TipsHandler (webapp2.RequestHandler):
    def get(self):
        tips_template = jinja_env.get_template('templates/tips.html')
        self.response.write(tips_template.render())

class UserSearch(ndb.Model):
    firstname = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)
    comments = ndb.StringProperty(required=True)

class ContactHandler (webapp2.RequestHandler):
    def get(self):
        contact_template = jinja_env.get_template('templates/contact.html')
        self.response.write(contact_template.render())

app = webapp2.WSGIApplication([
    ('/', SignInHandler),
    ('/music', MusicHandler),
    ('/gifs', GifsHandler),
    ('/tips', TipsHandler),
    ('/contact', ContactHandler),
], debug=True)
