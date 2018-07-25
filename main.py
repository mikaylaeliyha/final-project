import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# marie's login

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        me =  users.get_current_user()
        print "hi"
        print me
        start_template = jinja_current_dir.get_template("templates/main.html")
        jinja_values = {}

        if not me:
            jinja_values["signin_page_url"] = users.create_login_url('/')
        else:
            jinja_values["signout_page_url"] = users.create_logout_url('/')
        print jinja_values
        # else:
        #         'signin_page_url': users.create_logout_url('/'),
        #     }
        self.response.write(start_template.render(jinja_values))
        # else:
        #     my_key = ndb.Key('Visitor', me.user_id())
        #     my_visitor = my_key.get()
        #     if not my_visitor:
        #         my_visitor = Visitor(key = my_key, name = me.nickname(), email = me.email(),id = me.user_id(),
        #         page_view_count = 0)
        #     my_visitor.page_view_count += 1
        #     my_visitor.put()
        #     withuser_template = jinja_current_dir.get_template("templates/login.html")
        #     jinja_values = {
        #         'name': me.nickname(),
        #         'email_addr': me.email(),
        #         'user_id': me.user_id(),
        #         'signout_page_url': users.create_logout_url('/'),
        #         'number_of_views': my_visitor.page_view_count
        #     }
        #     self.response.write(withuser_template.render(jinja_values))

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

class ContactHandler (webapp2.RequestHandler):
    def get(self):
        contact_template = jinja_env.get_template('contact.html')
        self.response.write(contact_template.render())

# also added login handler to this
app = webapp2.WSGIApplication([
    ('/', SignInHandler),
    ('/login', SignInHandler),
    ('/music', MusicHandler),
    ('/gifs', GifsHandler),
    ('/tips', TipsHandler),
    ('/contact', ContactHandler),
], debug=True)
