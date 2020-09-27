# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint(name='api', import_name=__name__)

from . import views

