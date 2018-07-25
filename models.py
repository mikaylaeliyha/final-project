from google.appengine.ext import ndb

class Visitor(ndb.Model):
    name =  ndb.StringProperty(required=True)
    id =  ndb.StringProperty(required=True)
    email=  ndb.StringProperty(required=True)
