import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb
import smtplib

jinja_env = jinja2.Environment(
    loader= jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))

class MainHandler (webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('main.html')
        self.response.write(main_template.render())

class MusicHandler (webapp2.RequestHandler):
    def get(self):
        music_template = jinja_env.get_template('music.html')
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

        template = jinja_env.get_template('gifs.html')
        variables = {'gif_urls': gif_urls,
                    'q': search_term}
        self.response.write(template.render(variables))

    # gifs_template = jinja_env.get_template('gifs.html')
    # self.response.write(gifs_template.render())

class TipsHandler (webapp2.RequestHandler):
    def get(self):
        tips_template = jinja_env.get_template('tips.html')
        self.response.write(tips_template.render())

class UserSearch(ndb.Model):
    firstname = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)
    comments = ndb.StringProperty(required=True)

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        contact_template = jinja_env.get_template("contact.html")
        self.response.write(contact_template.render())
    def post(self):
        contact2_template = jinja_env.get_template("contact2.html")
        my_dict = {
            'firstname': self.request.get('firstname'),
            'lastname': self.request.get('lastname'),
            'country': self.request.get('country'),
            'comments': self.request.get('comments'),
        }
        story = UserSearch(firstname=my_dict["firstname"],lastname=my_dict["lastname"], country=my_dict["country"],
        comments=my_dict["comments"])
        story.put()
        self.response.write(contact2_template.render(my_dict))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/music', MusicHandler),
    ('/gifs', GifsHandler),
    ('/tips', TipsHandler),
    ('/contact', ContactHandler),
], debug=True)
