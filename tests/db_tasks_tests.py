import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from db.task_db import TaskDB,TaskState,TaskType
import config

class TestTaskDB(unittest.TestCase):        

    def setUp(self):
        self._taskDB = TaskDB('', 'zhihutest')
        self._taskDB.clear()

    def test_insertNew(self):
        id = 'test_insertNew'
        type = TaskType.People_Followers
        total = 5

        self._taskDB.insertNew(id, type, total)
        tasks = self._taskDB.findTasks(id, type)
        self.assertEqual(1, tasks.count())
        doc = tasks.next()
        self.assertIsNotNone(doc)
        self.assertEqual(id, doc['id'])
        self.assertEqual(type.name, doc['type'])
        self.assertEqual(0, doc['retry'])
        self.assertEqual(0, doc['done'])
        self.assertEqual(total, doc['total'])
        self.assertEqual(0, doc['start'])
        self.assertEqual(True, doc['isLast'])
        self.assertEqual(TaskState.Active.name, doc['state'])

    def test_insertNewTwice(self):
        taskDB = TaskDB('', 'zhihutest')
        taskDB.clear()

        id = 'test_insertNewTwice'
        type = TaskType.People_Followers

        taskDB.insertNew(id, type, 5)
        taskDB.insertNew(id, type, 5)

        tasks = taskDB.findTasks(id, type)
        self.assertEqual(1, tasks.count())

    def test_insertNewTotal0(self):
        taskDB = TaskDB('', 'zhihutest')
        taskDB.clear()

        id = 'test_insertNewTotal0'
        type = TaskType.People_Followers

        taskDB.insertNew(id, type, 0)
        self.assertEqual(False, taskDB.exists(id, type))

    def test_findActiveTask(self):
        taskDB = TaskDB('', 'zhihutest')
        taskDB.clear()

        task = taskDB.findActiveTask()
        self.assertIsNone(task)

        id = 'test_findActiveTask'
        type = TaskType.People_Followers
        total = 5

        taskDB.insertNew(id, type, total)
        self.assertEqual(True, taskDB.exists(id, type))
        task = taskDB.findActiveTask()
        self.assertIsNotNone(task)
        self.assertEqual(id, task['id'])
        self.assertEqual(type.name, task['type'])
        self.assertEqual(0, task['retry'])
        self.assertEqual(0, task['done'])
        self.assertEqual(total, task['total'])
        self.assertEqual(TaskState.Running.name, task['state'])

        return task

    def test_insertLargeTotalTask(self):
        id = 'test_insertLargeTotalTask'
        type = TaskType.People_Followers
        total = 201

        self._taskDB.insertNew(id, type, total)
        tasks = self._taskDB.findTasks(id, type)
        self.assertEqual(3, tasks.count())

        # 1st
        doc = tasks.next()
        self.assertIsNotNone(doc)
        self.assertEqual(id, doc['id'])
        self.assertEqual(total, doc['total'])
        self.assertEqual(0, doc['start'])
        self.assertEqual(False, doc['isLast'])
        self.assertEqual(TaskState.Active.name, doc['state'])

        # 2nd
        doc = tasks.next()
        self.assertIsNotNone(doc)
        self.assertEqual(id, doc['id'])
        self.assertEqual(total, doc['total'])
        self.assertEqual(100, doc['start'])
        self.assertEqual(False, doc['isLast'])
        self.assertEqual(TaskState.Active.name, doc['state'])

        # 3rd
        doc = tasks.next()
        self.assertIsNotNone(doc)
        self.assertEqual(id, doc['id'])
        self.assertEqual(total, doc['total'])
        self.assertEqual(200, doc['start'])
        self.assertEqual(True, doc['isLast'])
        self.assertEqual(TaskState.Active.name, doc['state'])

    def test_completeTask(self):
        task = self.test_findActiveTask()
        self._taskDB.completeTask(task['_id'])

        tasks = self._taskDB.findTasks(task['id'], TaskType.People_Followers)
        self.assertEqual(1, tasks.count())
        task = tasks.next()
        self.assertEqual(TaskState.Completed.name, task['state'])

if __name__ == '__main__':
    unittest.main()

