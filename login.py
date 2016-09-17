from __future__ import unicode_literals, print_function
import os
from zhihu_oauth import ZhihuClient
from zhihu_oauth.zhcls.people import People
from zhihu_oauth.zhcls.question import Question 
from zhihu_oauth.zhcls.generator import PeopleGenerator
import json
from db.mongo import User

TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

SKIP_FIELDS = [
    '_session'
]

GENERATOR_FIELDS = [
    'followers', 
    'followings', 
    'questions', 
    'following_columns',
    'answers',
    'articles',
    'columns',
    'activities',
    'following_questions',
    'collections',
    'following_collections',
    'following_topics']

def DumpUser(userObj):
    user = {}

    for k in [a for a in dir(userObj) if not a.startswith('__')]:
        if k in SKIP_FIELDS:
            pass
        elif k in GENERATOR_FIELDS:
            pass
        else:
            attr = getattr(userObj,k)
            if not callable(attr) and attr is not None:
                user[k] = attr

    return user

def PrintUser(user):
    for k in user:
        print('\'%s\' : %s' % (k, user[k]))

index = 0
loop = 5

def travelUser(user):
    global index
    if(index == 5):
        return

    print('-------------')
    print('[%d] %s' % (index, user.id))
    PrintUser(DumpUser(user))
    index = index + 1
    print('-------------\n')
    

    for follower in user.followers:
        travelUser(follower)

'''    
    for following in user.followings:
        travelUser(following)
'''
    

user = client.people('c4c8a4b3ac95dcb917a54ef945483c59')
#me = client.me()
#user = User(me)
#user.save_if_not_exist()

travelUser(user)