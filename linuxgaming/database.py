from flask import current_app
from pprint import pprint


def db_search(query={}):

    try:
        d = current_app.mongo.db.items.find(
            query
        ).sort('date', -1)
    except pymongo.errors.OperationFailure:
        print("DB Error")
        return False

    return d
