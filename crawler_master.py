# Encoding:UTF-8
import requests
import re


def login():
    url0 = 'https://www.zhihu.com/#signin'
    url1 = 'https://www.zhihu.com/login/email'
    login_data = {
        'email': '1430728487@qq.com',
        'password': 'hsc970501',
        'remember_me': 'true',
    }
    headers_signin = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;' +
        'q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0)' +
        ' Gecko/20100101 Firefox/45.0',
    }
    headers_base = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Length': 102,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0)' +
        ' Gecko/20100101 Firefox/45.0',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def getxsrf():
        r = requests.get(url0, headers=headers_signin)
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', r.text)
        return xsrf.group(0)

    xsrf = getxsrf()
    try:
        captcha_url = 'http://www.zhihu.com/captcha.gif'
        captcha = requests.get(captcha_url, stream=True)
        print(captcha)
        f = open('captcha.gif', 'wb')
        for line in captcha.iter_content(10):
            f.write(line)
        f.close()
        if f is not None:
            print(u'输入验证码：')
            captcha_str = input()
            login_data['captcha'] = captcha_str
    except:
        pass
    finally:
        pass
    login_data['_xsrf'] = xsrf.encode('utf-8')
    login = requests.post(url1, headers=headers_base, data=login_data)
    print(login)
    return login.cookies
