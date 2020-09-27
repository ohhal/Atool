# -*- coding: utf-8 -*-
"""
@Date : '2020-06-20'
@Desc :
"""
from flask import render_template

from . import admin


@admin.route('/admin/')
def index():
    return render_template('admin_base.html')