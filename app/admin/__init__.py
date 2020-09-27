# -*- coding: utf-8 -*-
"""
@Date : '2020-06-20'
@Desc :
"""
# -*- coding: utf-8 -*-
from flask import Blueprint

admin = Blueprint(name='admin', import_name=__name__)

from . import views