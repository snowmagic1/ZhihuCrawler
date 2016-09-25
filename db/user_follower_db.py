from enum import Enum
from pymongo import MongoClient
import logging

logger = logging.getLogger('userFollowerDB')

class UserFollowerDB:
    _collectionName = 'user_follower'

    def __init__(self, url, database='zhihu'):
        self._conn = MongoClient()
        self._db = self._conn[database]
        self. _collection = self._db[UserFollowerDB._collectionName]
    
    def clear(self):
        self._collection.delete_many({})

    def save(self, id, type, userIds):
        result = self._collection.insert_one({
                'id': id,
                'type':type,
                'userIDs': userIds
                })

        if result is None:
            logger.error('Failed to save [%s]' % id)
        else:
            logger.info('[%s] inserted' % id)