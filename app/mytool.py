# -*- coding: utf-8 -*-

import datetime
import json
import time
from io import BytesIO

import cv2
import numpy as np
import requests
from PIL import Image
from flask_mail import Message
from . import mail
from flask import url_for
from . import db
from .models import Commparam


def send_reset_mail(user):
    token = user.generate_auth_token()
    msg = Message("请求重置密码", sender='zalmailbox@qq.com', recipients=[user.email])
    msg.body = '''要重置密码，请访问以下链接：
    {}  
    如果您没有发出此请求，请忽略此电子邮件，不会进行任何修改'''.format(
        url_for('main.reset_token', token=token, _external=True))
    mail.send(msg)


def send_mail(user_mail, user):
    token = user.generate_auth_token()
    msg = Message("注册激活", sender='zalmailbox@qq.com', recipients=[user_mail])
    msg.body = '''激活该账号，请访问以下链接：
    {}  
    如果您没有发出此请求，请忽略此电子邮件'''.format(
        url_for('main.login_up_token', token=token, _external=True))
    mail.send(msg)


def generate_id(param_name):
    # 序号产生器
    dt = str(datetime.date.today()).replace('-', '')
    commparam = Commparam.query.filter_by(param_name=param_name).first()

    # 如果不存在,就创建
    if commparam is None:
        # 创建参数对象
        commparam = Commparam(param_name=param_name)
        # 提交数据库
        db.session.add(commparam)
        num = 1
    else:
        commparam.param_value += 1
        num = commparam.param_value
        db.session.add(commparam)

    id = '%s%08d' % (dt, num)

    return id


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def byte_arr(img_bytes):
    f = BytesIO()
    f.write(img_bytes)
    img_pil = Image.open(f)
    img_arr = np.asarray(img_pil)
    if len(img_arr.shape) > 2:
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
    return img_arr


def yzm(upload_path):
    time0 = time.time()
    with open(upload_path, "rb") as f:  # 二进制打开图片
        img_bin = f.read()
        res = {"image": list(img_bin)}
        r = requests.post('http://116.62.14.45:8888/', json=res) # 打码服务
        r_text = json.loads(r.text)
        r_text = r_text['code']
        ret = r_text
        time5 = time.time() - time0
        run_time = str(round(time5, 3))
        return ret, run_time
