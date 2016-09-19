from enum import Enum
from pymongo import MongoClient

SKIP_FIELDS = [
    '_session'
]

class GeneratorFileds(Enum):
    Followers = 'followers'
    Followings = 'followings' 
    Questions = 'questions'
    Following_columns = 'following_columns'
    Answers = 'answers'
    Articles = 'articles'
    Columns = 'columns'
    Activities = 'activities'
    Following_questions = 'following_questions'
    Collections = 'collections'
    Following_collections = 'following_collections'
    Following_topics = 'following_topics'

GENERATOR_FIELDS = [n.value for n in GeneratorFileds]

class UserDB:
    _collectionName = 'users'
   
    def __init__(self, url, database='zhihu'):
        self._conn = MongoClient()
        self._db = self._conn[database]
        self. _collection = self._db[UserDB._collectionName]

    def ToDict(self, user):
        user_dict = {}
        for k in [a for a in dir(user) if not a.startswith('__')]:
            if k in SKIP_FIELDS:
                pass
            elif k in GENERATOR_FIELDS:
                pass
            else:
                attr = getattr(user,k)
                if not callable(attr) and attr is not None:
                    user_dict[k] = attr

        return user_dict

    def ToString(self, user):
        text = ''
        for k in self.ToDict(user):
            text += ('\'%s\' : %s' % (k, self.Dict[k]))
            
        return text

    def clear(self):
        self._collection.delete_many({})

    def find_by_id(self, id):
        print('[db] find_by_id = [%s]' % id)
        user = self._collection.find_one({'id': id})

        return user

    def save_if_not_exist(self, user):
        user_dict = {}
        if isinstance(user, dict):
            user_dict = user
        else:
            user_dict = self.ToDict(user)

        print('[db] finding id = [%s]' % user_dict['id'])
        cursor = self._collection.find({'id': user_dict['id']}).limit(1)

        if(cursor.count() == 0):
            self._collection.insert_one(user_dict)
    
