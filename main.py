from flask import Flask, render_template, redirect, request
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user
from models import db, PersonageModel, EnemyModel, UserModels
from threading import Event, Thread
from forms import RegForm, LoginForm


import os, random

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = "this_badass_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


login_manager = LoginManager(app)


# функция - загрузчик пользователей
# без нее не работает функция login_user
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserModels).get(user_id)

idle_messages=["Ничего не происходит.",
          "Тишина...",
          "Нет новостей - хорошая новость"]
battle_messages=["{} сражается за свою жизнь!",
          "Сеча лютая, {} бьется отчаянно!",
          "{} рубится без остановки!"]
dead_messages=["{} разлагается физически",
          "Червяк ползет по ребру {} уже второй час",
          "{} переворачивается в гробу"]

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()
    user1 = PersonageModel("Alan Parson")
    user2 = PersonageModel("Elaine Dawson")
    user3 = PersonageModel("James White")
    user4 = PersonageModel("Joanne Rowling")
    enemy1 = EnemyModel("Чужой")
    enemy2 = EnemyModel("Радиоактивный таракан")
    enemy3 = EnemyModel("Кротокрыс")
    enemy4 = EnemyModel("Болотник")
    db.session.add_all([user1,user2,user3,user4])
    db.session.add_all([enemy1, enemy2, enemy3, enemy4])
    db.session.commit()

@app.route("/login", methods=['post', 'get'])
def login():
    form = LoginForm()  # добавляем форму
    username = ""
    password = ''
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModels.query.filter_by(username=username).first_or_404()
        if user:
            if user.check_password(password):
                # авторизация
                login_user(user, remember=False)
                return redirect("/userpage")
            else:
                print('Неправильный пароль')

    return render_template('login.html', form=form)


@app.route("/signup", methods=['post', 'get'])
def signup():
    form = SignupForm()
    username = ""
    email = ''
    password = ''
    password2 = ''
    if form.validate_on_submit():
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if UserModels.query.filter_by(username=username).first():
            return render_template('reg.html', form=form, message="Пользователь существует")
        if UserModels.query.filter_by(email=email).first():
            return render_template('reg.html', form=form, message="Email зарегистрирован")
        if password == password2:
            user = UserModels(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        else:
            return render_template('reg.html', form=form, message="Пароли не совпадают")
    return render_template('reg.html', form=form)

@app.route("/personages")
def list_personages():
    personages = PersonageModel.query.all()
    return render_template("personages.html",personages=personages)

@app.route("/enemies")
def list_enemies():
    enemies = EnemyModel.query.all()
    return render_template("enemies.html", enemies=enemies)

@app.route("/personage/<p_id>",methods=["POST","GET"])
def pers_page(p_id):
    if request.method == "GET":
        personage = PersonageModel.query.filter_by(id=p_id).first_or_404()
        return render_template("personage.html",personage=personage)
    if request.method == "POST":
        personage = PersonageModel.query.filter_by(id=p_id).first_or_404()
        db.session.delete(personage)
        db.session.commit()
        return redirect("/personages")

@app.route("/enemy/<p_id>",methods=["POST","GET"])
def enemy_page(p_id):
    if request.method == "GET":
        enemy = EnemyModel.query.filter_by(id=p_id).first_or_404()
        return render_template("enemy.html",enemy=enemy)
    if request.method == "POST":
        enemy = EnemyModel.query.filter_by(id=p_id).first_or_404()
        db.session.delete(enemy)
        db.session.commit()
        return redirect("/enemies")

@app.route("/personage",methods=["POST","GET"])
def create_personage():
    if request.method == 'GET':
        return render_template("personage_create.html")
    if request.method == 'POST':
        name=request.form['name']
        if 'file' not in request.files:
            flash('No file part')
            return render_template("personage_create.html")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template("personage_create.html")
        if file:
            os.mkdir(f"static/img/{name}")
            file.save(os.path.join(f"static/img/{name}","avatar.png"))
        pers=PersonageModel(name)
        db.session.add(pers)
        db.session.commit()
        return redirect("/personages")

@app.route("/personage/<p_id>/modify",methods=["POST","GET"])
def modify_personage(p_id):
    if request.method == "GET":
        personage = PersonageModel.query.filter_by(id=p_id).first_or_404()
        return render_template("personage_modify.html",personage=personage)
    if request.method == "POST":
        name = request.form['name']
        if 'file' not in request.files:
            flash('No file part')
            return render_template("personage_create.html")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template("personage_create.html")
        if file:
            try:
               os.mkdir(f"static/img/{name}")
            except:
                print('Directory already created')
            file.save(os.path.join(f"static/img/{name}", "avatar.png"))
        personage = PersonageModel.query.filter_by(id=p_id).first_or_404()
        personage.name=name
        personage.avatar_path=f"img/{name}/avatar.png"
        db.session.add(personage)
        db.session.commit()
        return redirect("/personages")

@app.route("/")
@app.route("/index")
def index():
    m=random.choice(idle_messages)
    return render_template("game.html",message=m)

@app.route("/battle/<p_id>")
def battle(p_id):
    personage = PersonageModel.query.filter_by(id=p_id).first_or_404()
    enemy=PersonageModel.query.filter_by(id=1).first_or_404()
    return render_template("battle.html",personage=personage, enemy=enemy)

@app.route("/dead/<p_id>")
def dead(p_id):
    m = random.choice(dead_messages)
    return render_template("game.html", message=m)

@app.route("/api/update/<p_id>")
def update(p_id):
    personage = PersonageModel.query.filter_by(id=p_id).first_or_404()
    if personage.state == 'idle':
        return {"status": 200, "message": random.choice(idle_messages), "hero":personage.json()}
    if personage.state == 'battle':
        return {"status": 200, "message": random.choice(battle_messages).format(personage.name) + str(personage.hp),"hero":personage.json()}
    if personage.state == 'dead':
        return {"status": 200, "message": random.choice(dead_messages).format(personage.name) + str(personage.hp),"hero":personage.json()}


def call_repeatedly(interval, func, *args):
    stopped = Event()
    counter=1
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
            print(counter)
    Thread(target=loop).start()
    return stopped.set

def game_loop():
    with app.app_context():
        personages = PersonageModel.query.all()
        for personage in personages:
            personage.money += 1
            personage.experience += 2
            if personage.state=='idle':
                if random.randint(1,100)<=5:
                    personage.state="battle"
                    print(personage.state,personage.name)
            elif personage.state == 'battle':
                enemy = EnemyModel.query.filter_by(id=1).first_or_404()
                #TODO5 функцию попадания для всех
                if personage.is_attack_succesfull(enemy):
                    enemy.hp-=random.randint(1,10)
                if (random.randint(0,enemy.strength+enemy.perception)>
                        random.randint(0,personage.endurance + personage.agility)):
                    personage.hp-=random.randint(1,10)
                if personage.hp>0 and enemy.hp<=0:
                    personage.state = 'idle'
                    personage.experience += 10
                    print(personage.state, personage.name)
                if personage.hp<=0:
                    personage.state='dead'
                    print(personage.state, personage.name)
            elif personage.state == 'dead':
                if personage.money >= 25 and personage.experience >= 50:
                    personage.state = ""
                    personage.hp = personage.max_hp
                    personage.money -= 25
                    personage.experience -= 25
                    personage.state = "idle"
                else:
                    personage.state = 'dead'
                    personage.money += 1
                    personage.experience += 2
            elif personage.state=="heal":
                pass
                #TODo4
            db.session.add(personage)
        db.session.commit()

cancel_future_calls = call_repeatedly(10, game_loop)

app.run()