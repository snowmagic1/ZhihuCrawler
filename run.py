from crawler.zh_user import UserFetcher
from crawler.fetcher import Fetcher

fetcher = UserFetcher()
fetcher.run('c4c8a4b3ac95dcb917a54ef945483c59')

f = Fetcher()
f.run()

print('done')