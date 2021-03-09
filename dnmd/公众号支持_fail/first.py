# -*- encoding:utf-8 -*-

import requests
import json


class SendMessage():
    def __init__(self):
        self.appID = 'wx540b10f2d152e6be'
        self.appsecret = 'eb467d5af2dd6cc8e7f65e00417c106f'
        self.access_token = self.get_access_token()
        # self.opend_ids = self.get_openid()

    def get_access_token(self):
        """
        获取微信公众号的access_token值
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
            format(self.appID, self.appsecret)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        # print(access_token)
        return access_token

    def get_openid(self):
        """
        获取所有粉丝的openid
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (self.access_token, next_openid)
        ans = requests.get(url_openid)
        print(ans.content)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    def sendmsg(self, msg):
        """
        给所有粉丝发送文本消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(self.access_token)
        print(url)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                    "touser": open_id,
                    "msgtype":"text",
                    "text":
                    {
                        "content": msg
                    }
                }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")

    def upload_media(self, media_type, media_path):
        """
        上传临时文件到微信服务器，并获取该文件到meida_id
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}'.format(self.access_token, media_type)
        print(url)
        meida = {
            'media': open(media_path, 'rb')
        }
        rsponse = requests.post(url, files=meida)
        parse_json = json.loads(rsponse.content.decode())
        print(parse_json)
        return parse_json.get('media_id')

    def send_media_to_user(self, media_type, media_path):
        """
        给所有粉丝发送媒体文件，媒体文件以meida_id表示
        """
        media_id = self.upload_media(media_type, media_path)
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}'.format(self.access_token)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                if media_type == "image":
                    body = {
                        "touser": open_id,
                        "msgtype": "image",
                        "image":
                            {
                                "media_id": media_id
                            }
                    }
                if media_type == "voice":
                    body = {
                        "touser": open_id,
                        "msgtype": "voice",
                        "voice":
                            {
                                "media_id": media_id
                            }
                    }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")


#     def upload_new_media(self, media_path):
#         url = f'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.access_token}'
#         meida = {
#             'media': open(media_path, 'rb')
#         }
#         html = requests.post(url, files=meida)
#         print(html.text)
#         print(html)
#     def uploadnews(self):
#         url = f'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token={self.access_token}'
#         data = {
#    "articles": [
#         {
#             "thumb_media_id":"",
#             "author":"",
#             "title":"Happy Day",
#             "content_source_url":"",
#             "content":"content",
#             "digest":"digest",
#             "show_cover_pic":0,
#             "need_open_comment":1,
#             "only_fans_can_comment":1
#         },
#         {
#             "thumb_media_id":"qI6_Ze_6PtV7svjolgs-rN6stStuHIjs9_DidOHaj0Q-mwvBelOXCFZiq2OsIU-p",
#             "author":"xxx",
#             "title":"Happy Day",
#             "content_source_url":"www.qq.com",
#             "content":"content",
#             "digest":"digest",
#             "show_cover_pic":0,
#             "need_open_comment":1,
#             "only_fans_can_comment":1
#         }
#    ]
# }
#         print(data)
#         html = requests.post(url, data=data)
#         print(html.text)
    def dyh_sendmsg(self, msg):
        url = f'https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={self.access_token}'
        print(self.access_token)
        data = {
    "filter": {
        "is_to_all": "False",
        "tag_id": "2"
    },
    "text": {
        "content": "CONTENT"
    },
    "msgtype": "text"
}
        html = requests.post(url, data=data)
        print(html)
        print(html.text)
if __name__ == "__main__":
    data = 'Hello,3Nod!'
    sends = SendMessage()
    # sends.get_access_token()
    # sends.get_openid()
    # sends.upload_new_media('C:/Users/zkxxx/Desktop/upload.PNG')
    # sends.uploadnews()
    sends.dyh_sendmsg(msg=data)
    # sends.send_media_to_user("image", './test.png')
    pass