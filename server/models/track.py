from base import BaseModel
from mongokit import Connection

class Track(BaseModel): 
    __collection__ = 'tracks'
       
    structure = {
        'track_id': int,
        'title' : basestring,
        'artist_info' : [{
            'artists' : [{
                'name': basestring,
                'type': basestring
            }],
            'artist_format' : basestring,
            'from_track' : int,
            'hidden': []
        }],
        'base_track': [],
        'modifier': {},
        'derivatives': [],
        'mixes': [],
        'tags': []
    }
    
    required = ['title', 'artist_info', 'track_id']
    
  
    def to_json(self):
        return {'track_name' : 'test', 'id': 123 }
