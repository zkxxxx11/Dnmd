# 微信公众号
import requests

from utils.log4 import Log
from utils.time_tools import current_str_time
import sys
import os
# 邮箱
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

logger = Log(name='notice.log').logger


def wechat_notice(title='Title', content=None):

    url = 'https://sc.ftqq.com/SCU147530T4ef14037d20165a4b4b8672c36b77a395ff7cd60e9b6f.send'
    params = {
        "text": f'[{current_str_time("%H:%M:%S")}]{title}',
        "desp": content
    }
    html = requests.get(url, params=params)
    # {"errno": 1024, "errmsg": "\u4e0d\u8981\u91cd\u590d\u53d1\u9001\u540c\u6837\u7684\u5185\u5bb9"}
    logger.info(html.text)
    if '"errno":0' in html.text:
        logger.info(f'<{title}> send to wechat success')
    else:
        logger.info(f'<{title}> send to wechat fail')



class Email():
    def __init__(self, mail_user, pwd):
        mail_user = '872146104@qq.com'
        pwd = ''
        mail_host = ''
        try:
            smtpObj = smtplib.SMTP()
            if mail_host:
                self.mail_host = mail_host
            elif mail_user.endswith('163.com'):
                self.mail_host = 'smtp.163.com'
            elif mail_user.endswith(('sina.com', 'sina.cn')):
                self.mail_host = 'smtp.163.com'
            elif mail_user.endswith('qq.com'):
                self.mail_host = 'smtp.qq.com'
            elif mail_user.endswith('sohu.com'):
                self.mail_host = 'smtp.sohu.com'
            else:
                self.mail_host = 'smtp.qq.com'
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(mail_user, pwd)
            self.mail_user = mail_user  # 我的邮箱
            self.is_login = True
        except Exception as e:
            print('login error')
        self.smtpObj = smtpObj
    def send(self, title, msg, receivers: list, img=''):
        """
        发送smtp邮件至收件人
        :param title:
        :param msg: 如果发送图片，需在msg内嵌入<img src='cid:xxx'>，xxx为图片名
        :param receivers:
        :param img: 图片名
        :return:
        """
        if self.is_login:
            message = MIMEMultipart('alternative')
            msg_html = MIMEText(msg, 'html', 'utf-8')
            message.attach(msg_html)
            message['Subject'] = title
            message['From'] = '872146104@qq.com'
            if img:
                with open(img, "rb") as f:
                    msg_img = MIMEImage(f.read())
                msg_img.add_header('content-ID', img)
                message.attach(msg_img)
            try:
                self.smtpObj.sendmail(self.mail_user, receivers, message.as_string())
                print('send success')
                logger.info(f'<{receivers}> send to qq success')
            except Exception as e:
                print('send fail')
                logger.info(f'<{receivers}> send to qq fail')
        else:
            print('not login')
            logger.info(f'not login')

# s = Email(mail_user='872146104@qq.com', pwd='')
# # s.send('111', 'message', receivers=['2231733504@qq.com', '872146104@qq.com'], 'img文件名')
# s.send('111', 'message', receivers=['2231733504@qq.com', '872146104@qq.com'])