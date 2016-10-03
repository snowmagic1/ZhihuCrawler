# os
import os
import json
import logging
import time
import datetime

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

    def __init__(self, taskDBUrl, userDBUrl, UserFollowerDBUrl):
        self._client = zhihuClient
        self._taskdb = TaskDB(taskDBUrl)
        self._userDB = UserDB(userDBUrl) 
        self._userFollowerDB = UserFollowerDB(UserFollowerDBUrl)
        self._scheduler = Scheduler(taskDBUrl, userDBUrl, UserFollowerDBUrl)
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
                except Exception:
                    logger.error('Failed to process task [%s] [%s]' % (task['type'], task['id']), exc_info=True)
                    self._taskdb.failTask(task)
                    continue

                self._taskdb.completeTask(task)

    def processTask(self, task):
        typeStr = task['type']
        type = TaskType.__members__[typeStr]
        id = task['id']
        logger.info('start to process task [%s] type: %s, id: %s' % (task['_id'], type.name, id))

        start = datetime.datetime.now()

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

        end = datetime.datetime.now()

        logger.info('Complete task [%s], duration [%s]ms' % (task['_id'], (end - start).seconds))

    def processPeople(self, id, userCollection, task):

        type = task['type']
        isLast = task['isLast']
        start = task['start']
        iterationNum = config.Task_Iteration_Item_Number

        userCollection.jump(start)
        index = 0
        userIDs = []

        logger.info('  %s : userid %s start %d isLast %d' % (type, id, start, isLast))
        for user in userCollection:

            if not isLast and index == (iterationNum):
                logger.debug('complete processing %s, userid %s' % (type, id))
                break

            index += 1

            # logger.info('#%d processing %s' % (index, user.id))
            userIDs.append(user.id)
            self._scheduler.QueueItem(user.id, TaskType.People, 1)

        self._userFollowerDB.save(user.id, type, userIDs)