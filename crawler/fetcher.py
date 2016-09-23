import os
import json
from db.user_db import UserDB
from .scheduler import Scheduler
from .zh_login import zhihuClient
from db.task_db import TaskType, TaskDB
import time

class Fetcher:

    def __init__(self):
        self._client = zhihuClient
        self._taskdb = TaskDB('')
        self._userDB = UserDB('') 
        self._scheduler = Scheduler()
        self._done = False
        self._index = 0;

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
            # self._scheduler.QueueItem(id, TaskType.People_Followers, user.follower_count)
            self._scheduler.QueueItem(id, TaskType.People_Followings, user.following_count)

        elif type == TaskType.People_Followers:
            user = self._client.people(id)
            self.processFollowersOrFollowings(id, user.followers, type)

        elif type == TaskType.People_Followings:
            user = self._client.people(id)
            self.processFollowersOrFollowings(id, user.followings, type)

        else:
            print('[Fetcher]: unknown task type %s' % type)

    def processFollowersOrFollowings(self, id, userCollection, type):
        for follower in userCollection:
            print('-----------------')
            print('%d [Fetcher] %s: %s' % (self._index, type.name, follower.id))
            self._index += 1
            # print(self._userDB.ToString(follower))
            print('-----------------')

            self._userDB.save(follower)
            # self._scheduler.QueueItem(follower.id, TaskType.People_Followers, follower.follower_count)
            # self._scheduler.QueueItem(follower.id, TaskType.People_Followings, follower.following_count)