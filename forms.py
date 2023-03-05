from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length,Email

class RegForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username",validators=[DataRequired(),])
    password = PasswordField("Password",validators=[DataRequired(), Length(min=5,max=100)])
    password_repeat = PasswordField("Repeat the password", validators=[DataRequired(), Length(min=5,max=100)])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), ])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5,max=100)])
    submit = SubmitField()
    '''
    def validate_password_confirm(form, field):
        if password.data!=password_repeat.data:
            raise ValidationError('Passwords should be same')
    '''