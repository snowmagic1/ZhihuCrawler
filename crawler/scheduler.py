import logging

from db.task_db import TaskDB, TaskType, TaskState
from db.user_db import UserDB
from db.user_follower_db import UserFollowerDB

logger = logging.getLogger('scheduler')

class Scheduler:

    def __init__(self, taskDBUrl, userDBUrl, UserFollowerDBUrl):
        self._taskdb = TaskDB(taskDBUrl)
        self._userdb = UserDB(userDBUrl)
        self._userFollowerdb = UserFollowerDB(UserFollowerDBUrl)

    def QueueItem(self, id, taskType, total):
        if total == 0:
            logger.debug('ignored task [%s] due to total is 0' % id)
            return

        exist = False
        if taskType == TaskType.People:
            exist = self._userdb.exists(id)
        elif taskType == TaskType.People_Followers or taskType == TaskType.People_Followings:
            exist = self._userFollowerdb.exists(id, taskType)

        if exist:
            logger.error('id [%s] type [%s] already exists' % (id, taskType.name))
        else:
            self._taskdb.insertNew(id, taskType, total)
            logger.info('Queued task [%s] [%s]' % (id, taskType.name))