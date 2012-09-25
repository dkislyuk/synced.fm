from base import BaseModel

class Tag(BaseModel): 
    __collection__ = 'tags'
       
    structure = {
        'track_id' : int,
        'user_id'  : basestring,
        'email'    : basestring,
    }
