from base import BaseModel

# Tracklists are ADTs used for all other track collections
class Tracklist(BaseModel):   
    structure = {
        'tracklist' : [basestring],
        'artist' : basestring
    }
    
    required_fields = ['tracklist', 'artist']

class Set(Tracklist):
    __collection__ = 'sets'
    
    structure = {
        'date' : basestring
    }
    
    required_fields = ['date']

class Episode(Tracklist):
    pass

class Mix(Tracklist):
    pass

class Playlist(Tracklist):
    pass

