from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    request,
    )
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
    )
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
# @login_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data.get('username', None)
        password = form.data.get('password', None)
        remember_me = form.data.get('remember_me')

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            flash(u'欢迎你：{}！'.format(user.username))
            login_user(user)
            # 登录后跳转到登陆前所在页面
            next = request.args.get('next')
            # 如果 next 为空或包含域名，判断为不合法的参数
            if next == None or url_parse(next).netloc != '':
                return redirect(url_for('index'))
            else:
                return redirect(next)
        else:
            flash(u'用户名或密码错误！')

        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你，注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/test')
@login_required
def test():
    return 'test page!'