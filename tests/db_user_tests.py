import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from db.mongo import User 

class TestUsersDB(unittest.TestCase):

    def test_user(self):
        user = {
            'answer_count':1,
            'articles_count': 0,
            'business' : {},
            'collected_count' : 0,
            'collection_count' : 1,
            'column_count' : 0,
            'columns_count' : 0,
            'created_at' : 1454652185,
            'description' : '',
            'educations' : [],
            'email' : 'snow_10151@outlook.com',
            'employments' : [],
            'favorite_count' : 1,
            'favorited_count' : 0,
            'follower_count' : 0,
            'following_column_count' : 0,
            'following_count' : 1,
            'following_question_count' : 2,
            'following_topic_count' : 10,
            'friendly_score' : 5.0,
            'gender' : 1,
            'headline' : '',
            'id' : '0532b5cb897016845f81f244cdfffcf7',
            'is_active' : True,
            'is_baned' : False,
            'is_locked' : False,
            'is_moments_user' : 0,
            'locations' : [],
            'name' : 'snowmagic1',
            'question_count' : 0,
            'shared_count' : 0,
            'thanked_count' : 0,
            'uid' : '678941155312406528',
            'voteup_count' : 1
        }

        return user

    def test_save(self):
        User.clear()

        user = self.test_user()
        user_dbo = User(user)
        user_dbo.save_if_not_exist()

        retrivedUser = User.find_by_id(user['id'])
        self.assertIsNotNone(retrivedUser)

if __name__ == '__main__':
    unittest.main()

