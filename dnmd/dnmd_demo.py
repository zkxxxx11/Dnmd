import requests
import re

from fake_useragent import UserAgent

from utils.log4 import Log
from utils.notice_tools import wechat_notice, Email


class Dnmd(object):
    def __init__(self):
        self.session = ''
        self.retry_time = 0
        self.user_name = ''
        self.retry_time = 0
        self.log_header = '[dnmd]'
        self.proxy = ''
        self.unitId = ''
        self.email = ''
        self.logger = Log(name='dnmd.log').logger
        self.headers = {
            # 'Host': 'baodao.zjsru.edu.cn',
            'User-Agent': UserAgent().random,
            # 'Referer': 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/login.aspx',
            # 'Cookie': 'td_cookie=3551128149; ASP.NET_SessionId=2sb2caxes1wk51bswkyjalap'
        }

    def login(self, **kwargs):
        psw = kwargs.get('psw')
        self.unitId = kwargs.get('id')
        self.email = kwargs.get('email')
        self.session = requests.session()
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/login.aspx'
        html = self.session.get(url, headers=self.headers)
        # print(html.text)
        view_state_gen = re.findall('EGENERATOR\" value=\"(.*?)\"', html.text)[0]
        view_state = re.findall('__VIEWSTATE\" value=\"(.*?)\"', html.text)[0]
        event_val = re.findall('EVENTVALIDATION\" value=\"(.*)\"', html.text)[0]
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/login.aspx'
        data = {
            '__EVENTVALIDATION': event_val,
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': view_state_gen,
            'BT_Login': '',
            'CB_Remeber': 'on',
            'TB_Psw': psw,
            'TB_User': self.unitId
        }
        # ip_port = get_random_proxy(retry_time=self.retry_time)
        # self.retry_time += 1
        # self.proxy = {
        #     "http": f"http://{ip_port}"}
        # self.proxy = {
        #     "http": f"http://202.105.181.195:28395"}

        html = self.session.post(url, data=data, headers=self.headers, allow_redirects=False, )
        self.logger.info(f'{self.log_header}[{self.unitId}][第{self.retry_time}次][login][ip:{self.proxy}][{html}]')
        if html.status_code == 500 or html.status_code == 503:
            self.retry_time += 1
            self.login(**kwargs)
            return False
        reback = re.findall('default\',content: \'(.*?)\'', html.text)
        if reback:
            self.logger.info(f'login fail: {self.unitId} {reback[0]}')
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
                # clock_status = 'tttttttttttt'
                if clock_status == '已打卡':
                    self.logger.info(
                        f'{self.log_header} id:{self.unitId} 打卡状态:{clock_status} 姓名:{self.user_name} 无需在打卡')
                    if self.email:
                        Email().send('打卡通知', f'{self.log_header}{self.user_name} 您今日已打卡 无需在打卡',
                                     receivers=[self.email])

                else:
                    self.logger.info(f'{self.log_header}[打卡状态:{clock_status}][姓名:{self.user_name}][开始打卡]')
                    self.submit()

            except Exception as e:
                self.logger.info(f'{self.log_header} Error: {self.unitId} get status failed')
                return False
        else:
            raise ValueError(f'login fail {html} please retry')

        #     'Cookie': 'td_cookie=3515120023; ASP.NET_SessionId=2sb2caxes1wk51bswkyjalap; YB_ILL2020=ID=34271&UID=201705021128'
        #     # 'Cookie: td_cookie=3516570089; ASP.NET_SessionId=2sb2caxes1wk51bswkyjalap; YB_ILL2020=ID=33613&UID=201705021118

        # get info

    def submit(self, max_retry_time=5):
        self.logger.info(f'{self.log_header}submiting........................')
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/DaKa_Normal_Simp.aspx'
        html = self.session.get(url)
        # print(html)
        hd_cid = re.findall('1_HD_CID\" value=\"(.*?)\"', html.text)[0]
        hd_id = re.findall('ContentPlaceHolder1_HD_ID\" value=\"(.*?)\"', html.text)[0]
        view_state_gen = re.findall('EGENERATOR\" value=\"(.*?)\"', html.text)[0]
        view_state = re.findall('__VIEWSTATE\" value=\"(.*?)\"', html.text)[0]
        event_val = re.findall('EVENTVALIDATION\" value=\"(.*)\"', html.text)[0]
        # self.logger.info(f'hd_cid:{hd_cid} \n hd_id:{hd_id} \n view_state:{view_state}'
        #                  f'\n view_state_gen:{view_state_gen} \n event_val:{event_val}')
        # 提交-------------------------------
        url = 'http://baodao.zjsru.edu.cn/ILL_COLLEGE/DaKa_Normal_Simp.aspx'
        data = {
            'ctl00$ContentPlaceHolder1$RBL_HS_TEST': '0',  # 是否做过核酸测试
            'ctl00$ContentPlaceHolder1$RBL_YQ': '否',
            'ctl00$ContentPlaceHolder1$CB_BAKE': '8',  # 低风险地区
            'ctl00$ContentPlaceHolder1$CB_CN': 'on',
            'ctl00$ContentPlaceHolder1$BT_Save': '今日打卡与昨日无异',
            'ctl00$ContentPlaceHolder1$HD_ID': hd_id,  # cookie内的id
            'ctl00$ContentPlaceHolder1$HD_UID': self.unitId,
            'ctl00$ContentPlaceHolder1$HD_CID': hd_cid,
            '__VIEWSTATE': view_state,
            # '__VIEWSTATEGENERATOR': '6043A07E',
            '__VIEWSTATEGENERATOR': view_state_gen,
            '__EVENTVALIDATION': event_val,
        }
        # data = {'ctl00%24ContentPlaceHolder1%24RBL_HS_TEST': '0',
        #         'ctl00%24ContentPlaceHolder1%24RBL_YQ': '否',
        #         'ctl00%24ContentPlaceHolder1%24CB_BAKE': '8',
        #         'ctl00%24ContentPlaceHolder1%24CB_CN': 'on',
        #         'ctl00%24ContentPlaceHolder1%24BT_Save': '今日打卡与昨日无异',
        #         'ctl00%24ContentPlaceHolder1%24HD_ID': '31407',
        #         'ctl00%24ContentPlaceHolder1%24HD_UID': '201705021416',
        #         'ctl00%24ContentPlaceHolder1%24HD_CID': '6556609',
        #         '__EVENTTARGET': '',
        #         '__EVENTARGUMENT': '', '__LASTFOCUS': '',
        #         '__VIEWSTATE': '/wEPDwULLTEzMzg5NTA4OTRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQpDQl9SZW1lYmVyYYJtCuU5oVMcE3qc93vMF87s2abhgUkd3fEPwhRgaRI=',
        #         '__VIEWSTATEGENERATOR': view_state_gen,
        #         '__EVENTVALIDATION': '/wEdAAUVulv2C6deMCR9/hjljoOjheBguD1NUPbgn4gAOnj59Qacqxe9WDw7v9hrSt6OV4XIaY/wumMLyCwxm7HL+uSflbeI2w157wKtP2wwi8fx9xTR51T/+9cfxbB1YXl+7H3QzuZ7IdYBIjyz0Yo5HIOW'}

        # print(self.session.cookies)
        # print('test:', data)
        # ip_port = get_random_proxy(retry_time=self.retry_time)
        # self.retry_time += 1
        # proxy = {
        #     "http": f"http://{ip_port}"}
        html = self.session.post(url, data=data, headers=self.headers)
        if html.status_code == 200:
            # print(html.text)
            if '您今日已成功打卡' in html.text or '您今日已打卡' in html.text:
                self.logger.info(f'{self.log_header}{self.user_name} 您今日已成功打卡')
                # wechat_notice(title=f'{self.log_header}{self.user_name} 您今日已成功打卡')
                if self.email:
                    Email().send('打卡通知', f'{self.log_header}{self.user_name} 您今日已成功打卡',
                                 receivers=[self.email])



            else:
                self.logger.info(f'{self.log_header}{self.user_name} 打卡失败')
        else:
            if self.retry_time < max_retry_time:
                self.logger.info(f'第{self.retry_time}次 submit ip:{self.proxy} 打卡失败 {html}')
                self.retry_time += 1
                # ip_port = get_random_proxy(retry_time=self.retry_time)
                # self.proxy = {
                #     "http": f"http://{ip_port}"}
                self.submit()
            else:
                self.logger.info(f'Error:超过{max_retry_time}次 submit ip:{self.proxy} 打卡失败 {html}')
                return False


if __name__ == '__main__':
    s = Dnmd()
    user_infos = {
        'zk': {'id': '201705021128',
               'psw': '119019',
               'email': ''},
        'wsx': {'id': '201705021118',
                'psw': '311610',
                # 'email': '2231733504@qq.com'
                },
        'jsc': {'id': '201705021416',
                'psw': '07181x',
                # 'email': '1838544232@qq.com'
                },
        'xh': {'id': '201705021121',
               'psw': '13001X'
               },
        'jlf': {'id': '201705021113',
                'psw': '090534',
                # 'email': '1341699342'
                }
    }
    s.login(**user_infos.get('jlf'))