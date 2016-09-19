import os
import json
from db.user_db import UserDB

from .zh_login import zhihuClient

class UserFetcher:

    def __init__(self):
        self._client = zhihuClient
        self._userDB = UserDB('') 

    def run(self, userid):
        user = zhihuClient.people(userid)
        self._userDB.save(user)

# user = zhihuClient.people('c4c8a4b3ac95dcb917a54ef945483c59')
#me = client.me()
#user = User(me)
#user.save_if_not_exist()