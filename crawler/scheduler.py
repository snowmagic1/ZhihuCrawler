from db.task_db import TaskDB, TaskType, TaskState

class Scheduler:

    def __init__(self):
        self._taskdb = TaskDB('')
    
    def QueueItem(self, id, taskType):
        exists = self._taskdb.exists(id, taskType)

        if(exists):
            print('task [%s] already exists' % id)
        else:
            self._taskdb.insertNew(id, taskType)