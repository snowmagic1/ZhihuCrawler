import os
from zhihu_oauth import ZhihuClient

TOKEN_FILE = 'token.pkl'

global zhihuClient 
zhihuClient = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    zhihuClient.load_token(TOKEN_FILE)
    print('login successfully')
else:
    zhihuClient.login_in_terminal()
    zhihuClient.save_token(TOKEN_FILE)