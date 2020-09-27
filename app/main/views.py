# -*- coding: utf-8 -*-
from datetime import datetime

from flask import (redirect, render_template,
                   url_for, flash, session, make_response)
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from . import main
from .forms import LoginForm, RegisterForm, ResetPasswordForm, RequestResetForm, ActMailForm
from ..config.Vcode import vc
from ..models import User, Article, db
from ..mylogger import logger
from ..mytool import generate_id, send_reset_mail, send_mail


# 主页
@main.route('/')
def index():
    logger.info('index')
    articles = Article().query.all()
    return render_template('index.html', articles=articles, flag=1)


# 登陆注册激活
@main.route('/login_in/', methods=['POST', 'GET'])
def login_in():
    form = LoginForm()
    logger.debug('用户登录')
    if form.submit.data:
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(user_name=username).first()
        if user.check_is_active():
            if user is not None and user.verify_password(password):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('main.index'))
            else:
                flash('用户名或密码不正确,请检查!', 'login_in')
                return render_template('login.html', form=form)
        else:
            flash('该账号邮箱未激活，请激活后重试!', 'login_in')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


# 注册
@main.route('/login_up/', methods=['GET', 'POST'])
def login_up():
    registerForm = RegisterForm()
    logger.debug('用户注册')
    if registerForm.submit.data:
        username = registerForm.username.data
        user = User.query.filter_by(user_name=username).first()
        if user:
            flash('用户名已存在', 'login_up')
            return render_template('login_up.html', form=registerForm)
        email = registerForm.email.data
        email_user = User.query.filter_by(email=email).first()
        if email_user:
            flash('该邮箱已经注册', 'login_up')
            return render_template('login_up.html', form=registerForm)
        passwd1 = registerForm.password.data
        passwd2 = registerForm.password2.data
        user_crt_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if passwd1 != passwd2:
            flash('两次密码不一致，请从新输入！', 'login_up')
            return render_template('login_up.html', form=registerForm)
        user = User(user_name=username, email=email, password=passwd1, user_crt_dt=user_crt_dt)
        user.user_id = generate_id('user')
        db.session.add(user)
        db.session.commit()
        try:
            send_mail(email, user=user)
        except Exception:
            db.session.delete(user)
            db.session.commit()
            flash('发送邮件失败，请检查邮件是否正确或者稍后重试', 'login_up')
            return render_template('login_up.html', form=registerForm)
        else:
            flash('发送激活邮件成功，请根据提示激活登陆', 'login_up')
            return render_template('login_up.html', form=registerForm)
    return render_template('login_up.html', form=registerForm)


# 激活页面
@main.route('/login_up_act/', methods=['GET', 'POST'])
def login_up_act():
    form = ActMailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_is_active():
            flash("该邮箱已经激活，请勿重复激活", 'login_up_act')
            return render_template('login_act.html', title='激活邮箱', form=form)
        try:
            send_mail(user_mail=form.email.data, user=user)
            flash("邮件发送成功，请进入邮件按提示激活后登陆", "login_in")
            return redirect(url_for('main.login_in'))
        except Exception:
            flash('邮件发送失败！', 'login_up_act')
            return render_template('login_act.html', title='激活邮箱', form=form)
    return render_template('login_act.html', title='激活邮箱', form=form)


# 激活
@main.route("/login_up/<token>", methods=['GET', 'POST'])
def login_up_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        flash('令牌已经过期，请重新获取！', "login_up")
        return redirect(url_for('main.login_up'))
    try:
        comment = User().query.filter_by(user_id=user.user_id).first()
        comment.is_activation = 1
        db.session.add(comment)
        db.session.commit()
    except:
        flash('激活失败，请重试！', "login_up")
        return redirect(url_for('main.login_up'))
    else:
        return redirect(url_for('main.login_in'))


# 检测需要登录的界面
@main.route('/login_out')
@login_required
def login_out():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


# 修改密码
@main.route("/reset_password/", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_mail(user)
            flash("邮件发送成功，请进入邮件按提示修改密码后登陆", "login_in")
            return redirect(url_for('main.login_in'))
        except Exception:
            flash('邮件发送失败！', 'reset_request')
            return render_template('reset_request.html', title='验证邮箱', form=form)
    return render_template('reset_request.html', title='验证邮箱', form=form)


# 修改密码认证
@main.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        flash('令牌已经过期，请重新获取！', "reset_request")
        return redirect(url_for('main.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password_hash = hashed_password
        db.session.commit()
        flash('密码修改成功，请使用新密码进行登陆', 'login_in')
        return redirect(url_for('main.login_in'))
    return render_template('reset_token.html', title='重置密码', form=form)


# 验证码
@main.route("/captcha/")
def verify_code():
    result = vc.generate()
    # 把验证码字符串保存到session
    session['code'] = vc.code
    # 创建响应对象
    response = make_response(result)
    response.headers["Content-Type"] = "image/png"
    return response
