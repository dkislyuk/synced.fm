from base import BaseModel
import hashlib

class MinLengthValidator(object):
    def __init__(self, min_length):
        self.min_length = min_length

    def __call__(self, value):
        if len(value) >= self.min_length:
            return True
        else:
            raise Exception('%s must be at least ' + str(self.min_length) + ' characters long.')

class User(BaseModel):
    __collection__ = 'users'

    structure = {
        'username' : basestring,
        'password' : basestring,
        'email'    : basestring,
    }

    validators = {
        'username' : MinLengthValidator(3)
    }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def set_password(self, password):
        self.password = "test"

    def to_json(self):
        return {'username' : self.username, 'email' : self.email}
