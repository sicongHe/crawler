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
print('Input ip adress:')
server_addr = input()
print('Connect to server %s...' % server_addr)

m = QueueManager(address=(server_addr, 5000), authkey=b'abc')

m.connect()

task = m.get_task_queue()
result = m.get_result_queue()
cookie = m.get_cookie_queue()
user = m.get_user_queue()


def work():
    url = task.get(timeout=100)
    print('Now working at ' + url)
    print('Task is running...')
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
    }
    headers_get['Referer'] = url.replace('/followees', '')
    logincookie = cookie.get(timeout=100)
    cookie.put(logincookie)
    getusers = requests.get(url, headers=headers_get, cookies=logincookie)
    final = re.findall(
        '\"https:\/\/www\.zhihu\.com\/people\/[a-zA-z0-9\-]+\"?',
        getusers.text,
    )
    n = task.qsize()
    if n < 200:
        for i in final:
            newtask = i.replace('\"', '') + '/followees'
            task.put(newtask)
            user.put(newtask)

    print('The task pool has %d tasks' % n)

while True:
    work()

print('Worker1 exit.')
