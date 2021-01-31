#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

import requests
import re
from fake_useragent import UserAgent
# wsx  2sb2caxes1wk51bswkyjalap
from utils.log4 import Log
from utils.notice_tools import wechat_notice
from utils.get_ip import get_random_proxy

class Dnmd(object):
    def __init__(self):
        self.session = ''
        self.retry_time = 0
        self.user_name = ''
        self.retry_time = 0
        self.log_header = '[dnmd]'
        self.logger = Log(name='dnmd.log').logger
    def login(self, id, psw):
        self.session = requests.session()
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/login.aspx'
        headers = {
            # 'Host': 'baodao.zjsru.edu.cn',
            'User-Agent': UserAgent().random,
            # 'Referer': 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/login.aspx',
            # 'Cookie': 'td_cookie=3551128149; ASP.NET_SessionId=2sb2caxes1wk51bswkyjalap'
        }
        data = {
            '__EVENTVALIDATION': '/wEdAAUzuAn+P9YHaOS+8lfGFdHnheBguD1NUPbgn4gAOnj59Qacqxe9WDw7v9hrSt6OV4XIaY/wumMLyCwxm7HL+uSflbeI2w157wKtP2wwi8fx9xP0n2aNKY9/zxxxutqiDzkce7tCin4VfGprN70h8t3S',
            '__VIEWSTATE': '/wEPDwULLTEzMzg5NTA4OTRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQpDQl9SZW1lYmVyeBR39cumdJBS3YuC1ek8HRuzlaxr37199LzjWCtmnnM=',
            '__VIEWSTATEGENERATOR': '46467A92',
            'BT_Login': '',
            'CB_Remeber': 'on',
            'TB_Psw': psw,
            'TB_User': id
        }

        ip_port = get_random_proxy(retry_time=self.retry_time)
        self.retry_time += 1
        proxy = {
            "http": f"http://{ip_port}"}
        html = self.session.post(url, data=data, headers=headers, allow_redirects=False,proxies=proxy)
        self.logger.info(f'第{self.retry_time}次 ip:{ip_port} login {html}')
        if html.status_code == 500 or html.status_code == 503:
            self.login(id, psw)
            return False

        reback = re.findall('default\',content: \'(.*?)\'', html.text)
        if reback:
            self.logger.info(f'login fail: {id} {reback[0]}')
            return False
        self.retry_time = 0
        # # cookie_dict = requests.utils.dict_from_cookiejar(html.cookies)
        # # print('cookie_dict:', cookie_dict)
        # # hd_id = cookie_dict.get('YB_ILL2020')[3:8]
        # # print('hd_id:', hd_id)
        html = self.session.get('http://baodao.zjsru.edu.cn/ILL_COLLEGE/index_Stu.aspx')
        # print(html.text)
        if html.status_code == 200:
            try:
                clock_status = 'unknow'
                self.user_name = re.findall('class=\"username\">(.*?)<', html.text)[0]
                clock_status = re.findall('vertical-align:middle;\">(.*?)<', html.text)[0]
                # clock_status = 'tttttttttttttttttttttttt'
                if clock_status == '已打卡':
                    self.logger.info(f'{self.log_header} id:{id} 打卡状态:{clock_status} 姓名:{self.user_name} 无需在打卡')
                    return False
                self.logger.info(f'{self.log_header} 打卡状态:{clock_status} 姓名:{self.user_name} 开始打卡')
                # self.submit()
            except Exception as e:
                if clock_status == '已打卡':
                    # raise ValueError(f'打卡状态:{clock_status} 姓名:{self.user_name}')
                    return False
                else:
                    self.logger.info(f'{id} get status failed')
                    # raise ValueError(f'get status failed')
                    return False
        else:
            raise ValueError(f'login fail {html} please retry')



        # get info
    def submit(self):
        self.logger.info('submiting........................')
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/DaKa_Normal_Simp.aspx'
        html = self.session.get(url)
        # print(html.text)
        # print(html)
        hd_cid = re.findall('1_HD_CID\" value=\"(.*?)\"', html.text)[0]
        hd_id = re.findall('ContentPlaceHolder1_HD_ID\" value=\"(.*?)\"', html.text)[0]
        #提交-------------------------------
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/DaKa_Normal_Simp.aspx'
        data = {
            'ctl00$ContentPlaceHolder1$RBL_HS_TEST': '0',  # 是否做过核酸测试
            'ctl00$ContentPlaceHolder1$RBL_YQ': '否',
            'ctl00$ContentPlaceHolder1$CB_BAKE': '8',  # 低风险地区
            'ctl00$ContentPlaceHolder1$CB_CN': 'on',
            'ctl00$ContentPlaceHolder1$BT_Save': '今日打卡与昨日无异',
            'ctl00$ContentPlaceHolder1$HD_ID': hd_id,  # cookie内的id
            'ctl00$ContentPlaceHolder1$HD_UID': id,
            'ctl00$ContentPlaceHolder1$HD_CID': hd_cid,
            '__VIEWSTATE': '/wEPDwUKMTA2NDEyODU2MQ9kFgJmD2QWAgIDD2QWAmYPZBYCAgEPZBYCZg9kFhRmDw8WAh4EVGV4dAUJ5rGf5oCd5oiQZGQCAQ8PFgIfAAUMMjAxNzA1MDIxNDE2ZGQCAg8PFgIfAAUS5L+h5oGv56eR5oqA5a2m6ZmiZGQCAw8PFgIfAAUY55S15a2Q5L+h5oGv5bel56iLMTcy54+tZGQCBA8PFgYfAAUG54Gw56CBHglGb3JlQ29sb3IKNB4EXyFTQgIEZGQCBQ8PFgYfAAUG54Gw56CBHwEKNB8CAgRkZAIGDw8WAh8ABQbnu7/noIFkZAIJDw8WAh8ABQbnu7/noIFkZAINDxBkZBYBAgFkAg4PZBYCZg9kFgICAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQVUVHlwZR4ORGF0YVZhbHVlRmllbGQFA1RJZB4LXyFEYXRhQm91bmRnZBAVAw/pq5jpo47pmanlnLDljLoP5Lit6aOO6Zmp5Zyw5Yy6D+S9jumjjumZqeWcsOWMuhUDATYBNwE4FCsDA2dnZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBR9jdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJENCX0NOSmY/0iO/GH/Z/Wu0nclh5adX+hbtAyp6wewL0+dvpKM=',
            # '__VIEWSTATEGENERATOR': '6043A07E',
            '__VIEWSTATEGENERATOR': '46467A92',
            '__EVENTVALIDATION': '/wEdABNYHIllq4wC2/B5oLh5pA1BZY5grL/efzX6cCKyrIYCV/hu4tvY6d9enkdKesu15kfq8+y4oTvW74GGIot0bIvICM3V+k7VCrmdV4Gfgjp7ZZ/8HIw0NLJDE4OyPzd76gcXlriPuyA18GqqYCJdVsKovuLlUH7eJOBwWX0pbtsX7P8VjaAM4vuVDz7oM+uNQ950nr+Y0+6ojLECDncBFgeD+4JvzNcxxgr1G28QRWVApx6qIg7qYhwFYzJyxC3qy8tyL6HWHRj3xizy22JGrI3lrRt2TLt9SA1rCjJNkv9zehv+ngOWuSM/KCfzF6nnGS6qzX+qeQPanSQlNiYM/Su4ufGzhwGQ1omcL+YXxMgCz4fAiR45fqjshjnPxEMaBL9iLVDGTJEp68yC0yf7FYK6J6BVphvslrBwTEbnE0TYHdPWKvNvZdQrb5XfbCSBjO4=',
            }
        # print('test:', data)
        html = self.session.post(url, data=data)
        if html.status_code == 200:
            # print(html.text)
            # print(html)
            if '您今日已成功打卡' in html.text:
                self.logger.info(f'{self.log_header}{self.user_name} 您今日已成功打卡')
                wechat_notice(title=f'{self.log_header}{self.user_name} 您今日已成功打卡')
            else:
                self.logger.info(f'{self.log_header}{self.user_name} 打卡失败')
        else:
            self.logger.info(f'{self.log_header}{self.user_name} 打卡失败{html}')

if __name__ == '__main__':
    s = Dnmd()
    # id = 'xxxxxxxxx'
    # psw = 'xxxxxxxxxx'
    #

    s.login(id, psw)