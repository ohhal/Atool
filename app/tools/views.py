# -*- coding: utf-8 -*-
"""
@Date : '2020-06-17'
@Desc :
"""
import os
import random
import string
import time

import requests
from PIL import Image
from flask import (render_template,
                   request)
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import tools
from ..mytool import allowed_file, yzm, byte_arr


@tools.route('/tools/')
@login_required
def tools_index():
    return render_template('tools.html')


@tools.route('/tools/<tools_id>/')
@login_required
def get_tools(tools_id):
    return render_template('tools_{}.html'.format(tools_id))


# ocr识别
@tools.route('/ocr', methods=['POST'])
@login_required
def tools_ocr():
    current_path = os.path.abspath(__file__)
    basepath = os.path.abspath(os.path.dirname(os.path.dirname(current_path)) + os.path.sep + ".")
    resultcode = 0
    resultmsg = '成功'
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basepath, 'static/tempfile',
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        ran_str = str(int(time.time())) + ''.join(random.sample(string.ascii_letters + string.digits, 20))
        if f and allowed_file(f.filename):
            f.save(upload_path)
            img = Image.open(upload_path)
            img_width, img_height = img.size
            img.save(upload_path)
        else:
            resultcode = -2
            resultmsg = "Please check the uploaded image type or img_url，Picture type is limited to png、PNG、jpg、JPG and bmp"
            return render_template('tools_ocr.html', resultcode=resultcode, resultmsg=resultmsg)
        try:
            result, run_time = yzm(upload_path)
        except Exception:
            resultcode = -3
            resultmsg = 'Error in identification process'
            return render_template('tools_ocr.html', resultcode=resultcode, resultmsg=resultmsg)
        if result:
            new_upload_path = os.path.join(basepath, 'static/tempfile',
                                           secure_filename(result + '_' + ran_str + '.png'))
            os.rename(upload_path, new_upload_path)
            src_path = './tempfile/' + result + '_' + ran_str + '.png'
            return render_template('tools_ocr.html', result=result, img_width=img_width, img_height=img_height,
                                   val1=time.time(), src_path=src_path, run_time=run_time, resultcode=resultcode,
                                   resultmsg=resultmsg)
        else:
            os.remove(upload_path)
            resultcode = -4
            resultmsg = 'Return result is empty'
            return render_template('tools_ocr.html', run_time=run_time, resultcode=resultcode, resultmsg=resultmsg)

    return render_template('tools_ocr.html')


@tools.route('/ocr_url', methods=['POST'])
@login_required
def tools_ocr_url():
    current_path = os.path.abspath(__file__)
    basepath = os.path.abspath(os.path.dirname(os.path.dirname(current_path)) + os.path.sep + ".")
    resultcode = 0
    resultmsg = '成功'
    if request.method == 'POST':
        input_ocr_type = 'imgurl'
        yzm_url = request.form.get('eid')
        ran_str = str(int(time.time())) + ''.join(random.sample(string.ascii_letters + string.digits, 20))
        if yzm_url:
            upload_path = os.path.join(basepath, 'static/tempfile',
                                       secure_filename(ran_str + '.png'))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            try:
                res = requests.get(yzm_url)
            except Exception:
                resultcode = -1
                resultmsg = 'Please check the img_url'
                return render_template('tools_ocr.html', resultcode=resultcode, resultmsg=resultmsg)
            arr_img = byte_arr(res.content)
            img_height, img_width = arr_img.shape[:2]
            with open(upload_path, 'wb') as f1:
                f1.write(res.content)
        else:
            resultcode = -2
            resultmsg = "Please check the uploaded image type or img_url，Picture type is limited to png、PNG、jpg、JPG and bmp"
            return render_template('tools_ocr.html', resultcode=resultcode, resultmsg=resultmsg)
        try:
            result, run_time = yzm(upload_path)
        except Exception:
            resultcode = -3
            resultmsg = 'Error in identification process'
            return render_template('tools_ocr.html', resultcode=resultcode, resultmsg=resultmsg)
        if result:
            new_upload_path = os.path.join(basepath, 'static/tempfile',
                                           secure_filename(result + '_' + ran_str + '.png'))
            os.rename(upload_path, new_upload_path)
            src_path = './tempfile/' + result + '_' + ran_str + '.png'
            return render_template('tools_ocr.html', result=result, img_width=img_width, img_height=img_height,
                                   val1=time.time(), src_path=src_path, run_time=run_time, resultcode=resultcode,
                                   resultmsg=resultmsg, input_ocr_type=input_ocr_type)
        else:
            os.remove(upload_path)
            resultcode = -4
            resultmsg = 'Return result is empty'
            return render_template('tools_ocr.html', run_time=run_time, resultcode=resultcode, resultmsg=resultmsg)

    return render_template('tools_ocr.html')

