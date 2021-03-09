import requests

from utils.log4 import Log

logger = Log(name='get_ip.log').logger


def get_random_proxy(retry_time=1):
    if retry_time < 5:
        url = '	http://api.shenlongip.com/ip'
        params = {
            'key':'walfjgse',
            'pattern':'txt',
            'count':'1',
            'protocol':'1'
        }
        html = requests.get(url, params=params)
        print(html.text.strip())
        return str(html.text.strip())
    else:
        logger('ip 不行了 失败超出设定次数')

# get_random_proxy(1)