# 微信公众号
import requests

from utils.log4 import Log
from utils.time_tools import current_str_time

logger = Log(name='notice.log').logger


def wechat_notice(title='Title', content=None):
    url = ''
    params = {
        "text": f'[{current_str_time("%H:%M:%S")}]{title}',
        "desp": content
    }
    html = requests.get(url, params=params)
    # {"errno": 1024, "errmsg": "\u4e0d\u8981\u91cd\u590d\u53d1\u9001\u540c\u6837\u7684\u5185\u5bb9"}
    logger.info(html.text)
    if '"errno":0' in html.text:
        logger.info(f'<{title}> send success')
    else:
        logger.info(f'<{title}> send fail')
