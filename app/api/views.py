# -*- coding: utf-8 -*-
"""
@Date : '2020-06-17'
@Desc :
"""
import requests
from flask import (request, jsonify)

from . import api


@api.route('/api/spider', methods=['POST'])
def spider_api():
    if request.method == 'POST':
        try:
            param_dict = eval(request.data)
            print(param_dict)
            url = param_dict['url']
            method = param_dict['method']
            requestformat = param_dict['requestformat']
            params = param_dict['params']
            headers = param_dict['headers']
            cookies = param_dict['cookies']
            proxy = param_dict['proxy']
        except Exception as e0:
            return jsonify(code=100000, msg='缺少必要参数 {}'.format(e0))
        else:
            if url:
                try:
                    res = get_url(url, method, headers, proxy, cookies, params, requestformat)
                except Exception as e:
                    if 'Failed to establish a new connection' in str(e):
                        return jsonify(code=100000, msg='由于目标计算机积极拒绝，无法连接。')
                    elif 'Invalid URL' in str(e):
                        return jsonify(code=100000, msg='Invalid URL')
                    elif 'Read timed out' in str(e):
                        return jsonify(code=100000, msg='请求超时')
                    else:
                        return jsonify(code=100000, msg='请求发送错误')
                else:
                    return jsonify(code=0, msg=res)
            else:
                return jsonify(code=100000, msg='请输入正确的url')
    else:
        return jsonify(code=100000, msg='请求必须为POST')


def get_url(url, method="GET", headers='', proxy='', cookies='', params='', requestformat='UTF-8'):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    if '\n' in headers:
        headers.replace('\n', '"').replace(' ', '"')
        headers = eval(headers)
    if '\n' in params:
        params.replace('\n','"').replace(' ','"')
    if method == 'POST':
        res = requests.post(url, headers=headers, timeout=10, proxies=proxies, cookies=cookies, data=params)
    else:
        res = requests.get(url, headers=headers, timeout=10, proxies=proxies, cookies=cookies, params=params)
    if requestformat == 'GBK':
        res.encoding = 'GBK'
    else:
        res.encoding = 'UTF-8'
    return res.text
