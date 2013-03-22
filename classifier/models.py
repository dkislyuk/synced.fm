from mongokit import Document
from mongokit import Connection
from mongokit import ObjectId

from conn import conn_str

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
    
    structure = {
      'name' : basestring,
      'config': {
                 'mfcc_step_size'    : int,
                 'mfcc_block_size'   : int,
                 'num_components'    : int,
                 'em_epsilon'        : float,
                 'em_iter'           : int,
                 'audio_freq'        : int,
                 'block_overlap'     : int,
                 'cv_type'           : basestring
                 },
      'data': []
      
    }
    
    def __iter__(self):
        connection = Connection(conn_str)
        connection.register([DataSet, TrackData])
        
        for track_id in self.data:
            track = connection.TrackData.one({"_id": ObjectId(track_id)})
            
            yield (track.label, track.data)
            
    def audio_block_size(self):
        frames_per_second   = self.config.audio_freq / self.config.mfcc_step_size
        audio_block_size    = self.config.block_overlap * frames_per_second
        return audio_block_size
