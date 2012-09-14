from mongokit import Connection
from mongokit import *
from models.track import Track
from models.event import Event
from models.tracklist import Set
from models.user import User

import sys, hashlib

class API(object):
    def __init__(self):
        self.connection = Connection('mongodb://admin:sync2200@staff.mongohq.com:10068/synced')
        self.connection.register([Track, Set, Event, User])
        pass
    
    # Track API
    def get_track(self, id):
        
        #return "got request"
        ret = self.connection.Event.find_one()

        return ret
    
    def create_track(self, params):
        print params

        x = self.connection.Track.from_json(params)
        print x
        x.save()
        sys.stdout.flush()
        
        
        return "OK"
 
    # User API   
    def create_user(self, params):        
        user = self.connection.User.from_json(params)
        user.password = hashlib.md5(user.password).hexdigest()
        
        
        user.save()
        
        sys.stdout.flush()
        return "OK"
    
    def get_user(self, id):
        pass