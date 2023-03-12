import random

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class PersonageModel(db.Model):
    __tablename__ = "personages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20), unique=True)
    strength = db.Column(db.Integer, nullable=False)
    perception = db.Column(db.Integer, nullable=False)
    endurance = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    intellect = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    luck = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    stimpacks = db.Column(db.Integer, nullable=False)
    avatar_path = db.Column(db.String(50))
    state = db.Column(db.String(10))

    def __init__(self, name):
        self.strength = random.randint(1, 2)
        self.perception = random.randint(1, 2)
        self.endurance = random.randint(1, 2)
        self.charisma = random.randint(1, 2)
        self.intellect = random.randint(1, 2)
        self.agility = random.randint(1, 2)
        self.luck = random.randint(1, 2)
        self.name = name
        self.max_hp = self.endurance * 10 + 20
        self.hp = self.max_hp
        self.money = random.randint(10, 20)
        self.experience = random.randint(10, 20)
        self.stimpacks = 2
        self.avatar_path = f"img/{self.name}/avatar.png"
        self.state = "idle"

    def set_user(self, user):
        self.user_id = user.id

    def __repr__(self):
        return f"{self.name} have {self.hp} of {self.max_hp} hp"

    def json(self):
        hero = {"S": self.strength,
                "P": self.perception,
                "E": self.endurance,
                # TODO3
                "hp": self.hp,
                "max_hp": self.max_hp}

        return hero

    # TODO2
    def is_attack_succesfull(self, obj):
        r = random.randint(0, 1)
        if r == 1:
            return True
        else:
            return False


class EnemyModel(db.Model):
    __tablename__ = "enemies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    strength = db.Column(db.Integer, nullable=False)
    perception = db.Column(db.Integer, nullable=False)
    endurance = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    intellect = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    luck = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)
    avatar_path = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name
        self.strength = random.randint(1, 2)
        self.perception = random.randint(1, 2)
        self.endurance = random.randint(1, 2)
        self.charisma = 0
        self.intellect = random.randint(1, 2)
        self.agility = random.randint(1, 2)
        self.luck = random.randint(1, 2)
        self.max_hp = self.endurance * 10 + 20
        self.hp = self.max_hp
        self.money = random.randint(10, 20)
        self.avatar_path = f"img/{self.name}/avatar.png"

    def __repr__(self):
        return f"{self.name} have {self.hp} of {self.max_hp} hp"

    # TODO1
    def json(self):
        pass


class UserModels(db.Model, UserMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    mail = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(50))
    personage = db.relationship('PersonageModel', backref='user', uselist=False)

    def __init__(self, username, email, password):
        self.login = username
        self.mail = email
        self.password = generate_password_hash(password)


    def __repr__(self):
        return 'Пользователь: '+self.username

    def __init__(self,username,email):
        self.username=username
        self.email=email

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
