from base import BaseModel
import datetime

from server import db
from config import Config
#from mongokit import Connection


class Track(BaseModel):
    __collection__ = 'tracks'

    structure = {
        'track_id': int,
        'title':    basestring,
        'artist_info': [{
            'artists': [{
                'name': basestring,
                'type': basestring
            }],
            'artist_format': basestring,
            'from_track': int,
            'hidden': []
        }],
        'base_track': [],
        'modifier': {},
        'derivatives': [],
        'mixes': [],
        'tags': [],
        'date_creation': datetime.datetime
    }

    required = ['title', 'artist_info', 'track_id']

    default_values = {
        'title': '',
        'date_creation': datetime.datetime.utcnow,
        'artist_info': [{
            'artists': [{
                'name': '',
                'type': 'primary'
            }],
            'artist_format': '',
            'from_track': 0
        }]
    }

    def initialize(self):
        self.track_id = db.get_connection([Config]).one()['track_id_count']
        db.get_connection([Config]).one().update({'$inc': {'track_id_count': 1}})

    def get_json(self):
        return self.return_fields(['title', 'artist_info'])
