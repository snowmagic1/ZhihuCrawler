
import os
import logging
import logging.config
import json
import argparse

import config
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

parser = argparse.ArgumentParser()
parser.add_argument("--mongodb", help="mongodb url",default=None)
args = parser.parse_args()

mongodbUrl = config.MongoDB_Default_Url
if not args.mongodb:
    mongodbUrl = args.mongodb
print('mongodb: [%s]' % mongodbUrl)

userdb = UserDB(mongodbUrl)
userdb.clear()

taskdb = TaskDB(mongodbUrl)
taskdb.clear()

userFollowerdb = UserFollowerDB(mongodbUrl)
userFollowerdb.clear()

scheduler = Scheduler(
    taskDBUrl=mongodbUrl,
    userDBUrl=mongodbUrl,
    UserFollowerDBUrl=mongodbUrl)

scheduler.QueueItem('c4c8a4b3ac95dcb917a54ef945483c59', TaskType.People, 1)

f = Fetcher(    
    taskDBUrl=mongodbUrl,
    userDBUrl=mongodbUrl,
    UserFollowerDBUrl=mongodbUrl)
f.run()

print('done')