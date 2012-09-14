from base import BaseModel

class Track(BaseModel): 
    __collection__ = 'tracks'
       
    structure = {
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
        'id': int,
        'modifier': {},
        'derivatives': [],
        'mixes': [],
    }
    
    def to_json(self):
        return {'user' : 'test', 'id': 123 }

