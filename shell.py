import os
import readline
from pprint import pprint

from flask import *
from server import *

from server.models.track import Track

ctx = app.test_request_context()
ctx.push()
os.environ['MONGOHQ_CONN'] = 'mongodb://admin:sync2200@staff.mongohq.com:10068/synced'
conn = db.get_connection([Track])


os.environ['PYTHONINSPECT'] = 'True'
