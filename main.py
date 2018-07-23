import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb

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
        gifs_template = jinja_env.get_template('gifs.html')
        self.response.write(gifs_template.render())
class TipsHandler (webapp2.RequestHandler):
    def get(self):
        tips_template = jinja_env.get_template('tips.html')
        self.response.write(tips_template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/music', MusicHandler),
    ('/gifs', GifsHandler),
    ('/tips', TipsHandler),
], debug=True)
