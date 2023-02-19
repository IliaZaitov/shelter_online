from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from form import LoginForm

user1={"name": "Илья", "password": "1234"}
user2={"name": "Ваня", "password": "12345"}
users=[user1, user2]

app=Flask(__name__)
app.config['SECRET_KEY'] = 'you_cant_guess_this_key'

@app.route("/", methods=["post","get"])
def index():
    form = LoginForm()
    username = ""
    password = ''
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        print(user1.get("name"), user1.get("password"))
        for i in range(len(users)):
            if username==users[i].get("name") and password==users[i].get("password"):
                return render_template('user_page.html', name=users[i].get("name"))
            elif username!=users[i].get("name") or password!=users[i].get("password"):
                return render_template('no_user_page.html')
    return render_template('index.html', form=form)
app.run(debug=True)