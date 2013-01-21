from mongokit import Document


class BaseModel(Document):
    __database__ = "synced"
    use_dot_notation = True
    use_autorefs = True

    structure = {}

    def get_json(self):
        return self.to_json()

    def in_test(self):
        return {"title":self['title']}

    def return_fields(self, keys):
        return dict(zip(keys, [self[key] for key in keys]))
