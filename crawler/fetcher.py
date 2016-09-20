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

    def run(self):
        task = self._taskdb.findActiveTask()

        if task is None:
            print('no active tasks, sleep for 10 seconds')
            time.sleep(10)
        else:
            typeStr = task['type']
            type = TaskType.__members__[typeStr]
            print('[fetcher] %s: %s' % (type.name, task['id']))
