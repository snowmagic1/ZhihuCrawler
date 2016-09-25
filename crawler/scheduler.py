import logging

from db.task_db import TaskDB, TaskType, TaskState

logger = logging.getLogger('scheduler')

class Scheduler:

    def __init__(self):
        self._taskdb = TaskDB('')
    
    def QueueItem(self, id, taskType, total):
        if(taskType is not TaskType.People and total == 0):
            logger.debug('ignored task [%s] due to total is 0' % id)
            return

        exists = self._taskdb.exists(id, taskType)

        if(exists):
            logger.error('task [%s] [%s] already exists' % (id, taskType.name))
        else:
            self._taskdb.insertNew(id, taskType, total)
            logger.info('task [%s] [%s] is queued' % (id, taskType.name))