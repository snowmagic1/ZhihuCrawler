import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from db.user_follower_db import UserFollowerDB
from db.task_db import TaskDB,TaskState,TaskType

class TestUserFollowerDB(unittest.TestCase):
    
    def setUp(self):
        self._followerDB = UserFollowerDB('', 'zhihutest')
        self._followerDB.clear()

    def test_save(self):
        ids = ['1', '2', '3']

        self._followerDB.save('123', TaskType.People_Followers.name, ids)

    def test_save2(self):
        ids = ['1', '2', '3']
        ids1 = ['123', '456', '111', '222']
        self._followerDB.save('123', TaskType.People_Followers.name, ids)
        self._followerDB.save('123', TaskType.People_Followers.name, ids1)

if __name__ == '__main__':
    unittest.main()

