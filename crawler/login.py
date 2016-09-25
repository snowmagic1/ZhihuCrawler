import os
import logging

from zhihu_oauth import ZhihuClient

logger = logging.getLogger('login')

TOKEN_FILE = 'token.pkl'

global zhihuClient 
zhihuClient = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    zhihuClient.load_token(TOKEN_FILE)
    logger.info('login successfully')
else:
    logger.info('login info is required')
    zhihuClient.login_in_terminal()
    zhihuClient.save_token(TOKEN_FILE)
    logger.info('login info has saved to %s' % TOKEN_FILE)