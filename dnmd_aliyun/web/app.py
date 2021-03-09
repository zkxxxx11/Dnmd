import json
import os
import sys

from flask import Flask, render_template, request

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from web.utils import get_conn

app = Flask(__name__)

@app.route('/thankyou')
def pay():
    return render_template('pay.html')
    
@app.route('/', methods=['get'])
def get_home():
    return render_template('tt1.html')


@app.route('/', methods=['POST'])
def add():
    # return render_template('index.html')
    scid = request.form['id']
    psw = request.form['psw']
    email = request.form['email']
    if len(scid) != 12 or len(psw) != 6:
        return '账号应为12位，密码应为六位 请重新添加'
    try:
        conn = get_conn()
        data = {
            'id': scid,
            'psw': psw,
            'email': email
        }
        # conn.lpush('tt', json.dumps(data))
        result = conn.setnx(scid, json.dumps(data))
        if result:
            resp = f'{scid} add success'
        else:
            conn.set(scid, json.dumps(data))
            resp = f'{scid} 已存在库中且更新为{data}'

    except Exception as e:
        raise Exception('error')
    return resp

# http://127.0.0.1:5000/1
# @app.route('/1')
# def hello_world1():
#     # return render_template('index.html')
#     return '11111'
if __name__ == '__main__':
    # app._static_folder = "./templates/static"
    # app.run(host='0.0.0.0',port=5000)
    app.run()