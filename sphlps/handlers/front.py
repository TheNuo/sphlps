# 主版块: 错误/注册/登录 等页面
# i love nuonuo
# auther:KRzhao

import os
from flask import Blueprint, render_template, url_for, redirect, flash, send_from_directory
from flask_login import login_user, logout_user, login_required
from ..models import User
from ..forms import RegisterForm, LoginForm

# 省略了 url_prefix, 默认值为 '/'
front = Blueprint('front', __name__)


@front.route('/')
def index():
    """ 主页页面 """
    return render_template('index.html')


@front.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册页面 """
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功, 请登录! ', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@front.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录页面 """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # 第一个参数是 User 对象, 第二个参数是个布尔值, 是否需要记住该用户
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))
