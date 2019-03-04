from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField
from wtforms import SubmitField, TextAreaField


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    pass


class SignInForm(FlaskForm):
    username = StringField('Придумайте логин', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    submit = SubmitField('Попробуйте зарегистрироваться')
    pass


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')
    pass
