import os
from flask import Flask

app = Flask(__name__)

from pymongo import Connection

connection = Connection('mongodb://admin:sync2200@staff.mongohq.com:10068/synced')
db = connection['synced']
config = db['config'].find_one()
idx_count = config['idx_count']
tracks = db['mixes']


@app.route('/')
def hello():
    return 'Hello World!' + str(idx_count)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    # port = int(os.environ.get('PORT', 5027))
    port = 5000
    app.run(host='0.0.0.0', port=port)
