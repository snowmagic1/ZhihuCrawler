import os
import json
from db.UserDB import UserDB

import domainObjects.login
zhihuClient = domainObjects.login.zhihuClient

index = 0
loop = 5

def travelUser(user):
    global index
    if(index == 5):
        return

    print('-------------')
    print('[%d] %s' % (index, user.id))
    userdb = UserDB(user)
    print(userdb)
    index = index + 1
    print('-------------\n')
    
    for follower in user.followers:
        travelUser(follower)

'''    
    for following in user.followings:
        travelUser(following)
'''

user = zhihuClient.people('c4c8a4b3ac95dcb917a54ef945483c59')
#me = client.me()
#user = User(me)
#user.save_if_not_exist()

travelUser(user)