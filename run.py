import logging

from crawler.scheduler import Scheduler
from crawler.fetcher import Fetcher

from db.task_db import TaskType, TaskDB
from db.user_db import UserDB
from db.user_follower_db import UserFollowerDB

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

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