from enum import Enum
from pymongo import MongoClient
from pymongo import ReturnDocument
import config
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
    _singleTaskTotal = config.Task_Iteration_Item_Number

    def __init__(self, url, database='zhihu'):
        self._conn = MongoClient()
        self._db = self._conn[database]
        self. _collection = self._db[TaskDB._collectionName]
    
    def insertNew(self, id, type, total):
        if type is not TaskType.People and total == 0:
            return

        taskNum = int(total/TaskDB._singleTaskTotal)

        for i in range(0, taskNum+1): 

            start = i*TaskDB._singleTaskTotal
            isLast = (i == taskNum)

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
            upsert=True,
            return_document=ReturnDocument.AFTER
            )

            if inserted is None:
                print('[taskDB]: Failed to insert [%s] [%s] [%d]' % (id, type.name, start))
            else:
                print('[taskDB]: Success inserted [%s] [%s] [%d]' % (id, type.name, start))

    def findTasks(self, id, type):
        return self._collection.find({'id':id, 'type':type.name})

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

    def completeTask(self, taskId):
        updated = self._collection.find_one_and_update(
            {
                '_id':taskId,
            },
            {
                '$set':
                {
                'state':TaskState.Completed.name,
                'endTime':str(datetime.datetime.now())
                }
            },
            return_document=ReturnDocument.AFTER
            )

        if updated is None or updated['state'] != TaskState.Completed.name:
            print('[taskDB]: Failed to complete task [%s]' % (taskId))
        else:
            print('[taskDB]: Success complete task [%s]' % (taskId))