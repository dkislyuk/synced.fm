from base import BaseModel

class DataSet(BaseModel):
    __collection__ = "dataset"
    skip_validation = True
    
    structure = {
      'name' : basestring,
      'data': [],
      's3_links': [],
      'status': basestring
    }
    
