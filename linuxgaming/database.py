from flask import current_app


def find_all(query={}):

    try:
        d = current_app.mongo.db.items.find(query).sort('date', -1)
    except Exception as e:
        current_app.logger.error('DB replace error %s', e)
        return False

    return d


def replace_one(query, data, upsert=True):

    try:
        current_app.mongo.db.items.replace_one(query, data, upsert)
    except Exception as e:
        current_app.logger.error('DB replace error %s', e)
        return False

    return True
