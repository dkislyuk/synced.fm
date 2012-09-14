from base import BaseModel
from tracklist import Set

class Event(BaseModel):
    __collection__ = 'events'
    
    structure = {
        'sets' : [Set]
    }
    
    

