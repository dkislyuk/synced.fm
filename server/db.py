import os
from mongokit import Connection
from mongokit import ObjectId
from flask import _app_ctx_stack


def init_app(app):
    app.teardown_appcontext(close_database_connection)


def get_connection(models_to_register):
    ctx = _app_ctx_stack.top
    con = getattr(ctx, 'synced_database', None)
    if con is None:
        con = Connection(os.environ['MONGOHQ_CONN'])
        con.register(models_to_register)
        ctx.synced_database = con
    return con


def close_database_connection(error = None):
    con = getattr(_app_ctx_stack.top, 'synced_database', None)
    if con is not None:
        con.close()

def find(model, object_id):
    return get_connection([model]).__getattr__(model.__name__).one({"_id": ObjectId(object_id)})
    