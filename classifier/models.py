from mongokit import Document
from mongokit import Connection
from mongokit import ObjectId

from conn import conn_str

import datetime

class SampleData(Document):
    __database__ = "synced"
    __collection__ = "gmm"
    use_dot_notation = True
    use_autorefs = True
    
    structure = {
      'title': basestring,
      'offset': int,
      'means': [],
      'covars': [],
      'weights': []
    }
    
class TrackData(Document):
    __database__ = "synced"
    __collection__ = "audio_samples"
    use_dot_notation = True
    use_autorefs = True
    
    structure = {
      'label': basestring,
      'set':   basestring, 
      'data' : []
    }   
    
class DataSet(Document):
    __database__ = "synced"
    __collection__ = "dataset"
    use_dot_notation = True
    use_autorefs = True
    #skip_validation = True
    
    structure = {
      'name' : basestring,
      'config': {
                 'mfcc_step_size'    : int,
                 'mfcc_block_size'   : int,
                 'num_components'    : int,
                 'em_epsilon'        : float,
                 'em_iter'           : int,
                 'audio_freq'        : int,
                 'sample_step_size'  : int,
                 'sample_length'     : int,
                 'cv_type'           : basestring
                 },
      'data': [],
      's3_links': [],
      'status': basestring,
      'created_at': datetime.datetime,
      'default_validation_score': float
    }
    
    default_values = {
      'created_at': datetime.datetime.utcnow,
      'config': {
        'mfcc_step_size'    : 256,
        'mfcc_block_size'   : 512,
        'num_components'    : 6,
        'em_epsilon'        : 0.001,
        'em_iter'           : 100,
        'audio_freq'        : 16000,
        'sample_length'     : 5,
        'sample_step_size'  : 1,
        'cv_type'           : 'diag'          
      },
     'default_validation_score': 0.0
    }
    
    def get_tracks(self):
        connection = Connection() if conn_str is None else Connection(conn_str)
        connection.register([TrackData])
        
        for track_id in self.data:
            track = connection.TrackData.one({"_id": ObjectId(track_id)})
            
            yield (track.label, track.data)
            
    def audio_block_size(self):
        frames_per_second   = self.config.audio_freq / self.config.mfcc_step_size
        audio_block_size    = self.config.sample_length * frames_per_second
        return audio_block_size
    
    def delete_data(self):
        connection = Connection() if conn_str is None else Connection(conn_str)
        connection.register([TrackData])
        
        for track_id in self.data:
            track = connection.TrackData.one({"_id": ObjectId(track_id)})
            track.delete()
            
        self.data = []
        self.status = "deleted"
        self.save()
        
    def get_json(self):
        return self.return_fields(['name', 'status'])
    
    def return_fields(self, keys):
        return dict(zip(keys, [self[key] for key in keys]))

            
