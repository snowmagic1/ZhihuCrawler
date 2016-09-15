from __future__ import unicode_literals, print_function
import os
from zhihu_oauth import ZhihuClient
import json

TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

index = 0

def travelUser(user):
    global index
    if(index == 100):
        return

    print('-------------')
    print('[%d] %s' % (index, user.id))
    print(user.name)
    index = index + 1

    for follower in me.followers:
        travelUser(follower)
    
    for following in user.followings:
        travelUser(following)

    print('-------------\n')

me = client.me()
#travelUser(me)
for k in [a for a in dir(me) if not a.startswith('__')]:
    attr = getattr(me,k)
    if not callable(attr) and attr is not None:
        print('\'%s\' : %s' % (k, attr))