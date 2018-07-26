import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Visitor

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        me =  users.get_current_user()
        print "hi"
        jinja_values = {}
        start_template = jinja_env.get_template("templates/main.html")
        if not me:
            jinja_values = {
                'signin_page_url': users.create_login_url('/')
            }
            self.response.write(start_template.render(jinja_values))
        else:
            my_key = ndb.Key('Visitor', me.user_id())
            my_visitor = my_key.get()
            if not my_visitor:
                my_visitor = Visitor(key = my_key, name = me.nickname(), email = me.email(),id = me.user_id())
            jinja_values["signout_page_url"] = users.create_logout_url('/')
            my_visitor.put()

        self.response.write(start_template.render(jinja_values))

class MainHandler (webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/main.html')
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
        query = SavedMethods.query(SavedMethods.id==users.get_current_user().user_id())
        self.response.write(tips_template.render({'data': query.get()}))

    def post(self):
        query = SavedMethods.query(SavedMethods.id==users.get_current_user().user_id())
        story = query.get()
        if not story:
            story = SavedMethods()
            story.id = users.get_current_user().user_id()

        story.click1 = self.request.get('click1')
        story.click2 = self.request.get('click2')
        story.click3 = self.request.get('click3')
        story.click4 = self.request.get('click4')
        story.click5 = self.request.get('click5')
        story.click6 = self.request.get('click6')
        story.click7 = self.request.get('click7')
        story.click8 = self.request.get('click8')
        story.click9 = self.request.get('click9')
        story.click10 = self.request.get('click10')
        story.click11 = self.request.get('click11')
        story.click12 = self.request.get('click12')
        story.click13 = self.request.get('click13')
        story.click14 = self.request.get('click14')
        story.click15 = self.request.get('click15')
        story.click16 = self.request.get('click16')
        story.click17 = self.request.get('click17')
        story.click18 = self.request.get('click18')

        tips2_template = jinja_env.get_template("templates/tips2.html")
        story.put()
        self.response.write(tips2_template.render())

class SavedMethods(ndb.Model):
    id =  ndb.StringProperty(required=True)
    click1 = ndb.StringProperty(required=False)
    click2 = ndb.StringProperty(required=False)
    click3 = ndb.StringProperty(required=False)
    click4 = ndb.StringProperty(required=False)
    click5 = ndb.StringProperty(required=False)
    click6 = ndb.StringProperty(required=False)
    click7 = ndb.StringProperty(required=False)
    click8 = ndb.StringProperty(required=False)
    click9 = ndb.StringProperty(required=False)
    click10 = ndb.StringProperty(required=False)
    click11 = ndb.StringProperty(required=False)
    click12 = ndb.StringProperty(required=False)
    click13 = ndb.StringProperty(required=False)
    click14 = ndb.StringProperty(required=False)
    click15 = ndb.StringProperty(required=False)
    click16 = ndb.StringProperty(required=False)
    click17 = ndb.StringProperty(required=False)
    click18 = ndb.StringProperty(required=False)

class SavedPage(webapp2.RequestHandler):
    def get(self):
        saved_template = jinja_env.get_template('templates/saved.html')
        query = SavedMethods.query(SavedMethods.id==users.get_current_user().user_id())
        self.response.write(saved_template.render({'data': query.get()}))


class UserSearch(ndb.Model):
    firstname = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)
    comments = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    updated = ndb.DateTimeProperty(auto_now=True)

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        contact_template = jinja_env.get_template("templates/contact.html")
        self.response.write(contact_template.render())
    def post(self):
        my_dict = {
            'firstname': self.request.get('firstname'),
            'lastname': self.request.get('lastname'),
            'email': self.request.get('email'),
            'country': self.request.get('country'),
            'comments': self.request.get('comments'),
            'updated_at': self.request.get('updated_at')
        }
        story = UserSearch(firstname=my_dict["firstname"],lastname=my_dict["lastname"], email=my_dict["email"],
        country=my_dict["country"], comments=my_dict["comments"])
        contact2_template = jinja_env.get_template("templates/contact2.html")
        story.put()
        self.response.write(contact2_template.render(my_dict))


class Contact3Handler(webapp2.RequestHandler):
    def get(self):
        contact3_template = jinja_env.get_template('templates/contact3.html')
        recentcomments = UserSearch.query().order(-UserSearch.updated_at).fetch(limit=10)
        self.response.write(contact3_template.render({'recentcomments': recentcomments}))

class DiscussionHandler (webapp2.RequestHandler):
    def get(self):
        discussion_template = jinja_env.get_template('templates/discussion.html')
        self.response.write(discussion_template.render())


app = webapp2.WSGIApplication([
    ('/', SignInHandler),
    ('/music', MusicHandler),
    ('/gifs', GifsHandler),
    ('/tips', TipsHandler),
    ('/contact', ContactHandler),
    ('/contact3', Contact3Handler),
    ('/saved', SavedPage),
    ('/discussion', DiscussionHandler),
], debug=True)
