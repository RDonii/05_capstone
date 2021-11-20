import os
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy import Column, String, Integer, create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import ForeignKey

load_dotenv()

database_name = 'meal'
database_path = "postgresql://{}:{}@{}:{}/{}".format(os.getenv('USER'),os.getenv('PASSWORD'),'localhost','5432',database_name)

db = SQLAlchemy()

def create_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class City(db.Model):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cafe = db.relationship('Cafe', backref='city')

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name
        }

class Cafe(db.Model):
    __tablename__ = 'cafe'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)

    def __init__(self, name, city_id):
        self.name = name
        self.city_id = city_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'city_id': self.city_id
        }
