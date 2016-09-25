from enum import Enum
import datetime
import logging

from pymongo import MongoClient
from pymongo import ReturnDocument

import config

logger = logging.getLogger('taskDB')

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
        if total == 0:
            logger.debug('ignored task [%s] [%s] due to total is 0' % (id, type))
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
                logger.error('Failed to insert [%s] [%s] [%d]' % (id, type.name, start))
            else:
                logger.debug('Task inserted [%s] [%s] start=[%d]' % (id, type.name, start))

    def findTasks(self, id, type):
        return self._collection.find({'id':id, 'type':type.name})

    def findTaskById(self, taskId):
        return self._collection.find_one({'_id':taskId})

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

    def completeTask(self, task):
        taskId = task['_id']
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
            logger.error('Failed to complete task [%s]' % (taskId))
        else:
            logger.info('Success complete task [%s]' % (taskId))
    
    def failTask(self, task):
        retry = int(task['retry'])
        update = {}

        if retry >= config.Task_Max_Retry_Number:
            logger.info('hit max retry count, abort task [%s] [%s]' % (task['type'], task['id']))
            update = {'$set': {
                        'state':TaskState.Aborted.name,
                        'endTime':str(datetime.datetime.now())}}
        else:
            logger.info('set task [%s] [%s] to active to retry' % (task['type'], task['id']))
            update = {'$set': {'state':TaskState.Active.name},
                      '$inc': {'retry':1}}

        updated = self._collection.find_one_and_update(
            {
                '_id':task['_id'],
            },
            update,
            return_document=ReturnDocument.AFTER
            )

        if updated is None:
            logger.error('Failed to fail task [%s]' % (task['id']))
        else:
            logger.info('Success fail task [%s]' % (task['id']))