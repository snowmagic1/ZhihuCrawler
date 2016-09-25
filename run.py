
import os
import logging
import logging.config
import json

from crawler.scheduler import Scheduler
from crawler.fetcher import Fetcher

from db.task_db import TaskType, TaskDB
from db.user_db import UserDB
from db.user_follower_db import UserFollowerDB

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG' ):

    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()

userdb = UserDB('')
userdb.clear()

taskdb = TaskDB('')
taskdb.clear()

userFollowerdb = UserFollowerDB('')
userFollowerdb.clear()

scheduler = Scheduler()
scheduler.QueueItem('c4c8a4b3ac95dcb917a54ef945483c59', TaskType.People, -1)

f = Fetcher()
f.run()

print('done')