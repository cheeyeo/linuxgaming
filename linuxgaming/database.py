"""
Database helpers

"""

from flask import current_app, abort


def find_all(query=None):
    """
    return mongodb cursor results from a find query

    :param query: the mongodb query
    :return: mongoDB cursor
    """

    try:
        data = current_app.mongo.db.items.find(query).sort('date', -1)
    except RuntimeError as error:
        current_app.logger.error('DB replace error %s', error)
        abort(500)

    return data


def replace_one(query, data, upsert=True):
    """
    Replace one document helper

    :param query: the mongodb query
    :param data: data to replace/insert
    :param upsert: insert if dociment doesn't exist
    :return: boolean
    """

    try:
        current_app.mongo.db.items.replace_one(query, data, upsert)
    except RuntimeError as error:
        current_app.logger.error('DB replace error %s', error)
        abort(500)

    return True
