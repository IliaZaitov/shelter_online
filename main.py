from flask import Flask, render_template, redirect, request, flash
from flask_cors import CORS
from models import db, PersonageModel
from threading import Event, Thread


import os, random

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
    db.session.add_all([user1,user2,user3,user4])
    db.session.commit()


@app.route("/personages")
def list_personages():
    personages = PersonageModel.query.all()
    return render_template("personages.html",personages=personages)

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
        return {"status": 200, "message": random.choice(idle_messages)}
    if personage.state == 'battle':
        return {"status": 200, "message": random.choice(battle_messages).format(personage.name) + str(personage.hp)}
    if personage.state == 'dead':
        return {"status": 200, "message": random.choice(dead_messages).format(personage.name) + str(personage.hp)}


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
            if personage.state=='idle':
                if random.randint(1,100)<=5:
                    personage.state="battle"
                    print(personage.state,personage.name)
            elif personage.state == 'battle':
                enemy = PersonageModel.query.filter_by(id=1).first_or_404()
                if (random.randint(0,personage.strength+personage.perception)>
                        random.randint(0,enemy.endurance + enemy.agility)):
                    enemy.hp-=random.randint(1,10)
                if (random.randint(0,enemy.strength+enemy.perception)>
                        random.randint(0,personage.endurance + personage.agility)):
                    personage.hp-=random.randint(1,10)
                if personage.hp>0 and enemy.hp<=0:
                    personage.state = 'idle'
                    print(personage.state, personage.name)
                if personage.hp<=0:
                    personage.state='dead'
                    print(personage.state, personage.name)
            db.session.add(personage)
        db.session.commit()

cancel_future_calls = call_repeatedly(10, game_loop)

app.run()