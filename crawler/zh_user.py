import os
import json
from db.user_db import UserDB
from .scheduler import Scheduler
from .zh_login import zhihuClient
from db.task_db import TaskType

class UserFetcher:

    def __init__(self):
        self._client = zhihuClient
        self._userDB = UserDB('') 
        self._scheduler = Scheduler()

    def run(self, userid):
        user = zhihuClient.people(userid)
        self._userDB.save(user)
        self._scheduler.QueueItem(userid, TaskType.People_Followers, user.follower_count)
        self._scheduler.QueueItem(userid, TaskType.People_Followings, user.following_count)