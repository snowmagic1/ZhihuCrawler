from enum import Enum
from pymongo import MongoClient
import datetime

class TaskType(Enum):
    People_Followings = 0,
    People_Followers = 1

class TaskState(Enum):
    Active = 0,
    Running = 1,
    Completed = 2,
    Aborted = 3

class TaskDB:
    _collectionName = 'tasks'
    _datetime_format = "%Y-%m-%d %H:%M"

    def __init__(self, url, database='zhihu'):
        self._conn = MongoClient()
        self._db = self._conn[database]
        self. _collection = self._db[TaskDB._collectionName]
    
    def insertNew(self, id, type, total):
        if total == 0:
            return
            
        ret = self._collection.insert_one({
            'id':id, 
            'type':type.name,
            'retry':0,
            'state':TaskState.Active.name,
            'total': total,
            'done':0,
            'scheduledTime':str(datetime.datetime.now())})

    def findExistingTask(self, id, type):
        doc = self._collection.find_one({'id':id, 'type':type.name})
        return doc

    def exists(self, id, type):
        cursor = self._collection.find({'id':id, 'type':type.name}).limit(1)
        return cursor.count() == 1

    def clear(self):
        self._collection.delete_many({})