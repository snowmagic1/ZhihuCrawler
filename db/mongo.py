from pymongo import MongoClient

client = MongoClient()
db = client.test

class User:
    def __init__(self, user):
        self._user = user

    @staticmethod
    def clear():
        db.users.delete_many({})

    def save_if_not_exist(self):
        print('[db] finding id = [%s]' % self._user['id'])
        cursor = db.users.find({'id': self._user['id']}).limit(1)

        if(cursor.count() == 0):
            db.users.insert_one(self._user)
    
    @staticmethod
    def find_by_id(id):
        print('[db] find_by_id = [%s]' % id)
        user = db.users.find_one({'id': id})

        return user