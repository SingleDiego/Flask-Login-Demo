from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired(message='请输入用户名。')]
        )
    email = StringField(
        'Email', 
        validators=[
        DataRequired(), 
        Email(message='邮箱格式不正确。')
        ]
        )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(message='请输入密码。')]
        )
    password2 = PasswordField(
        'Repeat Password', 
        validators=[
        DataRequired(message='请输入密码。'), 
        EqualTo('password', message='两次密码输入不一致。')
        ]
        )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'该用户名已存在，请选择其他用户名。')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(u'该邮箱已被注册，请选择其他邮箱，')