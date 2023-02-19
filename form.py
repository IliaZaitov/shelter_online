from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), ])
    username = StringField("Username",validators=[DataRequired(),])
    password = PasswordField("Password",validators=[DataRequired(),])
    submit = SubmitField()