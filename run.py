from crawler.scheduler import Scheduler
from crawler.fetcher import Fetcher
from db.task_db import TaskType, TaskDB
from db.user_db import UserDB

userdb = UserDB('')
userdb.clear()

taskdb = TaskDB('')
taskdb.clear()

scheduler = Scheduler()
scheduler.QueueItem('c4c8a4b3ac95dcb917a54ef945483c59', TaskType.People, -1)

f = Fetcher()
f.run()

print('done')