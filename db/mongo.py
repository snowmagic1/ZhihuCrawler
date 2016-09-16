from mongoengine import *

connect('ZhiHu')

class User(Document):
    answer_count = IntField()
    articles_count = IntField()
    created_at = DateTimeField()
    description = StringField()
    email = StringField()
    favorite_count = IntField()
    favorited_count = IntField()
    follower_count = IntField()
    following_count = IntField()
    following_question_count = IntField()
    following_topic_count = IntField()
    friendly_score = IntField()
    gender = BooleanField()
    headline = StringField()
    id = StringField()
    is_active = BooleanField()
    is_baned = BooleanField()
    is_locked = BooleanField()
    name = StringField()
    question_count = IntField()
    shared_count = IntField()
    thanked_count = IntField()
    uid = StringField()
    voteup_count = IntField()

    def __init__(self, user):
        self._user = user

    @staticmethod
    def clear():
        db.users.delete_many({})

    def save_if_not_exist(self):
        print('[db] finding id = [%s]' % self._user.id)
    
    @staticmethod
    def find_by_id(id):
        print('[db] find_by_id = [%s]' % id)
