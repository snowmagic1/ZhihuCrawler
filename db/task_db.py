from enum import Enum
from pymongo import MongoClient
from pymongo import ReturnDocument
import datetime

class TaskType(Enum):
    People = 0,
    People_Followings = 1,
    People_Followers = 2

class TaskState(Enum):
    Active = 0,
    Running = 1,
    Completed = 2,
    Aborted = 3

class TaskDB:
    _collectionName = 'tasks'
    _datetime_format = "%Y-%m-%d %H:%M"
    _singleTaskTotal = 100

    def __init__(self, url, database='zhihu'):
        self._conn = MongoClient()
        self._db = self._conn[database]
        self. _collection = self._db[TaskDB._collectionName]
    
    def insertNew(self, id, type, total):
        if type is not TaskType.People and total == 0:
            return

        taskNum = int(total/TaskDB._singleTaskTotal)

        for i in (0, taskNum): 

            start = i*taskNum
            isLast = (i == taskNum - 1)

            inserted = self._collection.find_one_and_update(
            {
                'type':type.name,
                'id':id,
                'start':start
            },
            {
                '$setOnInsert':
                {
                'id':id, 
                'type':type.name,
                'retry':0,
                'state':TaskState.Active.name,
                'total': total,
                'start':start,
                'isLast':isLast,
                'done':0,
                'createdOn':str(datetime.datetime.now()),
                'startTime':'',
                'endTime':''
                }
            },
            upsert=True
            )

    def findTasks(self, id, type):
        doc = self._collection.find_one({'id':id, 'type':type.name})
        return doc

    def exists(self, id, type):
        cursor = self._collection.find({'id':id, 'type':type.name}).limit(1)
        return cursor.count() == 1

    def clear(self):
        self._collection.delete_many({})

    def findActiveTask(self):
        task = self._collection.find_one_and_update(
                    {'state': TaskState.Active.name},
                    {'$set': {'startTime': str(datetime.datetime.now())}, 
                     '$set': {'state':TaskState.Running.name}
                    },
                    return_document=ReturnDocument.AFTER
                )
        
        return task