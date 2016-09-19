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
        self._scheduler.QueueItem(userid, TaskType.People_Followers)
        self._scheduler.QueueItem(userid, TaskType.People_Followings)

# user = zhihuClient.people('c4c8a4b3ac95dcb917a54ef945483c59')
#me = client.me()
#user = User(me)
#user.save_if_not_exist()