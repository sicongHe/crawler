# Encoding:UTF-8
import requests
import re
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
QueueManager.register('get_cookie_queue')
QueueManager.register('get_user_queue')

server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)

m = QueueManager(address=(server_addr, 5000), authkey=b'abc')

m.connect()

task = m.get_task_queue()
result = m.get_result_queue()
cookie = m.get_cookie_queue()
user = m.get_user_queue()


def work():
    url = user.get(timeout=100)
    name = url.replace('https://www.zhihu.com/people/', '')
    name = name.replace('/followees', '')
    url = url.replace('followees', 'about')
    headers_get = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;' +
        'q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/people/he-ti-cong',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) ' +
        'Gecko/20100101 Firefox/45.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    headers_get['Referer'] = url.replace('/followees', '/about')
    logincookie = cookie.get(timeout=100)
    cookie.put(logincookie)
    getusers = requests.get(url, headers=headers_get, cookies=logincookie)
    final = re.findall(
        '<strong>[0-9]*<\/strong>',
        getusers.text,
    )
    final = final[2:6]
    for i in range(0, 4):
        final[i] = final[i].replace('<strong>', '')
        final[i] = final[i].replace('</strong>', '')
    final.insert(0, name)
    result.put(final)
    print('Put a new user\'s data in the queue...')


while True:
    work()

print('Worker2 exit.')
