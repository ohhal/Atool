# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
# 会话保护等级
login_manager.session_protection = 'strong'
# 设置登录页面端点
login_manager.login_view = 'main.login_in'
login_manager.login_message = '你必须登陆后才能访问该页面'


def create_app(config_name):
    app = Flask(__name__,
                )

    app.config.update(dict(
        DEBUG=True,
        MAIL_SERVER='smtp.qq.com',
        MAIL_PORT=25,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME='944782440@qq.com',
        MAIL_PASSWORD='lnxejxiefuosbcgb',
    ))

    mail.init_app(app)

    # 初始化app配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 扩展应用初始化
    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    # 初始化蓝本
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .fiction import fiction as fiction_blueprint
    app.register_blueprint(fiction_blueprint)
    from .tools import tools as tools_blueprint
    app.register_blueprint(tools_blueprint)
    # 初始化api
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
