import os
import readline
from pprint import pprint

from flask import *
from server import *

from server.models.track import Track

ctx = app.test_request_context()
ctx.push()

os.environ['PYTHONINSPECT'] = 'True'
