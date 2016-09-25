# os
import os
import json
import logging
import time

# zhihu_auth
from .login import zhihuClient

# this project
from db.user_db import UserDB
from .scheduler import Scheduler
from db.task_db import TaskType, TaskDB
from db.user_follower_db import UserFollowerDB
import config

logger = logging.getLogger('fetcher')

class Fetcher:

    def __init__(self):
        self._client = zhihuClient
        self._taskdb = TaskDB('')
        self._userDB = UserDB('') 
        self._userFollowerDB = UserFollowerDB('')
        self._scheduler = Scheduler()
        self._done = False

    def run(self):
        
        while not self._done:
            task = self._taskdb.findActiveTask()
            if task is None:
                logger.debug('no active tasks, sleep for 10 seconds')
                time.sleep(10)
            else:
                try:
                    self.processTask(task)
                except Exception, e:
                    logger.error('Failed to process task [%s] [%s]' % (task['type'], task['id']), exc_info=True)
                    continue

                self._taskdb.completeTask(task['_id'])

    def processTask(self, task):
        typeStr = task['type']
        type = TaskType.__members__[typeStr]
        id = task['id']
        logger.info('start to process task %s: %s' % (type.name, id))

        if type == TaskType.People:
            user = self._client.people(id)

            self._userDB.save(user)
            self._scheduler.QueueItem(id, TaskType.People_Followers, user.follower_count)
            self._scheduler.QueueItem(id, TaskType.People_Followings, user.following_count)

        elif type == TaskType.People_Followers:
            user = self._client.people(id)
            self.processPeople(id, user.followers, task)

        elif type == TaskType.People_Followings:
            user = self._client.people(id)
            self.processPeople(id, user.followings, task)

        else:
            logger.error('unknown task type %s' % type)

        logger.info('End processing task %s: %s' % (type.name, id))

    def processPeople(self, id, userCollection, task):

        type = task['type']
        isLast = task['isLast']
        start = task['start']
        iterationNum = config.Task_Iteration_Item_Number

        userCollection.jump(start)
        index = 0
        userIDs = []

        for user in userCollection:

            if not isLast and index == (iterationNum):
                logger.debug('[Fetcher] complete processing task')
                break

            index += 1

            logger.debug('-----------------')
            logger.info('%d %s: %s' % (index, type, user.id))
            userIDs.append(user.id)

            # save to DB
            self._userDB.save(user)
            
            # queue items
            self._scheduler.QueueItem(user.id, TaskType.People_Followers, user.follower_count)
            self._scheduler.QueueItem(user.id, TaskType.People_Followings, user.following_count)

            logger.debug('-----------------')

        self._userFollowerDB.save(user.id, type, userIDs)