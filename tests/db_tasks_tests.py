import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from db.task_db import TaskDB,TaskState,TaskType

class TestTaskDB(unittest.TestCase):

    def test_insertNew(self):
        taskDB = TaskDB('', 'zhihutest')
        taskDB.clear()

        id = 'test_insertNew'
        type = TaskType.People_Followers
        total = 5

        taskDB.insertNew(id, type, total)
        self.assertEqual(True, taskDB.exists(id, type))
        doc = taskDB.findExistingTask(id, type) 
        self.assertIsNotNone(doc)
        self.assertEqual(id, doc['id'])
        self.assertEqual(type.name, doc['type'])
        self.assertEqual(0, doc['retry'])
        self.assertEqual(0, doc['done'])
        self.assertEqual(total, doc['total'])
        self.assertEqual(TaskState.Active.name, doc['state'])

    def test_insertNewTwice(self):
        taskDB = TaskDB('', 'zhihutest')
        taskDB.clear()

        id = 'test_insertNewTwice'
        type = TaskType.People_Followers

        taskDB.insertNew(id, type, 5)
        taskDB.insertNew(id, type, 5)

    def test_insertNewTotal0(self):
        taskDB = TaskDB('', 'zhihutest')
        taskDB.clear()

        id = 'test_insertNewTotal0'
        type = TaskType.People_Followers

        taskDB.insertNew(id, type, 0)
        self.assertEqual(False, taskDB.exists(id, type))

if __name__ == '__main__':
    unittest.main()
