from base import BaseModel

# Tracklists are ADTs used for all other track-aggregations
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
    __collection__ = 'episodes'
    
    structure = {
        'date' : basestring
    }
    
    required_fields = ['date']


class Mix(Tracklist):
    __collection__ = 'mixes'
    
    structure = {
        'date' : basestring
    }
    
    required_fields = ['date']


class Playlist(Tracklist):
    __collection__ = 'playlists'
    
    structure = {
        'date' : basestring
    }
    
    required_fields = ['date']

