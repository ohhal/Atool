# -*- coding: utf-8 -*-
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, \
    ValidationError
from wtforms.validators import DataRequired, Length, email, EqualTo, Email

from ..models import User

"""
字段类型      说　　明
StringField 文本字段
TextAreaField 多行文本字段
PasswordField 密码文本字段
HiddenField 隐藏文本字段
DateField 文本字段，值为 datetime.date 格式
DateTimeField 文本字段，值为 datetime.datetime 格式
IntegerField 文本字段，值为整数
DecimalField 文本字段，值为 decimal.Decimal
FloatField 文本字段，值为浮点数
BooleanField 复选框，值为 True 和 False
RadioField 一组单选框
SelectField 下拉列表
SelectMultipleField 下拉列表，可选择多个值
FileField 文件上传字段
SubmitField 表单提交按钮
FormField 把表单作为字段嵌入另一个表单
FieldList 一组指定类型的字段

验证函数 说　　明
Email 验证电子邮件地址
EqualTo 比较两个字段的值；常用于要求输入两次密码进行确认的情况
IPAddress 验证 IPv4 网络地址
Length 验证输入字符串的长度
NumberRange 验证输入的值在数字范围内
Optional 无输入值时跳过其他验证函数
Required 确保字段中有数据
Regexp 使用正则表达式验证输入值
URL 验证 URL
AnyOf 确保输入值在可选值列表中
NoneOf 确保输入值不在可选值列表中
"""


# 登陆
class LoginForm(FlaskForm):
    username = StringField(
        label='用户昵称',
        validators=[
            DataRequired("昵称必填"),
            Length(min=3, max=20, message="用户名必须介于3-20个字符")
        ],
        render_kw={"placeholder": "用户名必须介于3-20个字符"})
    password = PasswordField(
        label="用户密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '密码必须大于6个字符',
        })
    code = StringField(
        label="验证码",
        validators=[DataRequired('验证码格式错误'),
                    Length(min=4, max=4)],
        render_kw={
            "placeholder": "请输入验证码"
        }
    )

    # 自定义验证器来对生成的code验证
    def validate_code(self, field):
        # 取字段field对象上的值做验证
        # field.data等价于用户输入的值
        if field.data != session.get('code'):  # 获取session中生成的code
            raise ValidationError('验证码错误')

    remember_me = BooleanField(label='记住我', default=False)
    submit = SubmitField(label='登录')
    # submit_login_up = SubmitField(label='注册')


# 注册
class RegisterForm(FlaskForm):
    username = StringField(
        label='用户昵称',
        validators=[
            DataRequired("昵称必填"),
            Length(min=3, max=20, message="用户名必须介于3-20个字符")
        ],
        render_kw={"placeholder": "用户名必须介于3-20个字符"})
    password = PasswordField(
        label="用户密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '密码必须大于6个字符',
        })
    password2 = PasswordField(
        label="确认密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '再次输入',
        })
    email = StringField(
        '邮箱',
        validators=[email(message="邮箱格式不正确！")],
        render_kw={"placeholder": "E-mail: yourname@example.com"})
    submit = SubmitField(label='注册')


# 重置密码发送邮件
class RequestResetForm(FlaskForm):
    email = StringField(
        '邮箱',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "E-mail: yourname@example.com"})
    submit = SubmitField(label='验证邮箱')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('该邮箱不存在，请先注册')


# 重置密码
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        label="新密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '密码必须大于6个字符',
        })
    confirm_password = PasswordField(
        label="确认密码",
        validators=[DataRequired("密码必填！"), EqualTo('password')],
        render_kw={
            "placeholder": '再次输入',
        })
    submit = SubmitField(label='提交')

# 激活邮箱
class ActMailForm(FlaskForm):
    email = StringField(
        '邮箱',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "E-mail: yourname@example.com"})
    submit = SubmitField(label='激活邮箱')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('该邮箱不存在，请先注册')
