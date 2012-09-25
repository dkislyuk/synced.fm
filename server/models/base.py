from mongokit import Document

class BaseModel(Document):
    __database__ = "synced"
    use_dot_notation = True
    use_autorefs = True
    
    structure = {}