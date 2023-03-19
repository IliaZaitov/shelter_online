from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField()

class SignupForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    personage_name = StringField("Personage name", validators=[DataRequired(), ])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=100)])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField()


