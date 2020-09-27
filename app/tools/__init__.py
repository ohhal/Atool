# -*- coding: utf-8 -*-
from flask import Blueprint

tools = Blueprint(name='tools', import_name=__name__)

from . import views