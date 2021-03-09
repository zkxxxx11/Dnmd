import datetime

from utils.notice_tools import wechat_notice, Email
import sys
import os

current_date = datetime.datetime.now().strftime('%Y%m%d')
# print(current_date)
def send_log():
    try:
        file_name = f'dnmd{current_date}.log'
        with open(file_name, 'r', encoding='utf-8') as f:
            info = f.read()
        print(info)
        wechat_notice(title=file_name, content=info)
    except Exception as e:
        wechat_notice(title=f'{file_name}未生成！！！')







if __name__ == '__main__':
    send_log()
    # s = Email(mail_user='872146104@qq.com', pwd='')
    # # s.send('111', 'message', receivers=['2231733504@qq.com', '872146104@qq.com'], 'img文件名')
    # s.send('111', 'message', receivers=['2231733504@qq.com', '872146104@qq.com'])
    # try:
    #     file_name = f'dnmd{current_date}.log'
    #     file_path = os.path.abspath(os.path.dirname(__file__)) + f'{os.sep}utils{os.sep}log{os.sep}' + file_name
    #     with open(file_path, 'r', encoding='utf-8') as f:
    #         info = f.read()
    #     s.send(file_name, info, receivers=['872146104@qq.com'])
    # except Exception as e:
    #     s.send('Error', f'{file_name} 未生成', receivers=['872146104@qq.com'])

