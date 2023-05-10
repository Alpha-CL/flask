from app.extensions import db, DBModel
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DemoModel(DBModel):
    __tablename__ = "demo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(16))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=None)
    delete_time = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return "<DemoModel %r>" % f'{self.id}'
