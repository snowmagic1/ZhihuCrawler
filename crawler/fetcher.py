import os
import json
from db.user_db import UserDB
from .scheduler import Scheduler
from .zh_login import zhihuClient
from db.task_db import TaskType, TaskDB
import time
import config

class Fetcher:

    def __init__(self):
        self._client = zhihuClient
        self._taskdb = TaskDB('')
        self._userDB = UserDB('') 
        self._scheduler = Scheduler()
        self._done = False

    def run(self):
        
        while not self._done:
            task = self._taskdb.findActiveTask()
            if task is None:
                print('no active tasks, sleep for 10 seconds')
                time.sleep(10)
            else:
                self.processTask(task)
    
    def processTask(self, task):
        typeStr = task['type']
        type = TaskType.__members__[typeStr]
        id = task['id']
        print('[fetcher] %s: %s' % (type.name, id))

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
            print('[Fetcher]: unknown task type %s' % type)

    def processPeople(self, id, userCollection, task):

        type = task['type']
        isLast = task['isLast']
        start = task['start']
        iterationNum = config.Task_Iteration_Item_Number

        userCollection.jump(start)
        index = 0
        for follower in userCollection:

            if not isLast and index == (iterationNum -1):
                print('[Fetcher] complete processing task')
                break

            index += 1

            print('-----------------')
            print('%d [Fetcher] %s: %s' % (index, type, follower.id))
            # print(self._userDB.ToString(follower))
            print('-----------------')

            self._userDB.save(follower)
            # self._scheduler.QueueItem(follower.id, TaskType.People_Followers, follower.follower_count)
            # self._scheduler.QueueItem(follower.id, TaskType.People_Followings, follower.following_count)