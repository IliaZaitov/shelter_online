import random

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PersonageModel(db.Model):
    __tablename__ = "personages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique = True)
    strength = db.Column(db.Integer, nullable=False)
    perception = db.Column(db.Integer, nullable=False)
    endurance = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    intellect = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    luck = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer,nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)
    stimpacks = db.Column(db.Integer, nullable=False)
    avatar_path=db.Column(db.String(50))
    state=db.Column(db.String(10))

    def __init__(self, name):
        self.strength=random.randint(1,2)
        self.perception = random.randint(1, 2)
        self.endurance = random.randint(1, 2)
        self.charisma = random.randint(1, 2)
        self.intellect = random.randint(1, 2)
        self.agility = random.randint(1, 2)
        self.luck = random.randint(1, 2)
        self.name = name
        self.max_hp = self.endurance*10+20
        self.hp=self.max_hp
        self.money = random.randint(10,20)
        self.stimpacks=2
        self.avatar_path=f"img/{self.name}/avatar.png"
        self.state="idle"

    def __repr__(self):
        return f"{self.name} have {self.hp} of {self.max_hp} hp"