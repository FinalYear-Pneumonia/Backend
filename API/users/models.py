from API.extensions import database
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(database.Model):
    __tablename__ = "USER"
    public_id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    surname = database.Column(database.String(50), nullable=False)
    other_name = database.Column(database.String(100), nullable=False)
    birth_date = database.Column(database.Date, nullable=False)
    gender = database.Column(database.String(10), nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=True)
    contact = database.Column(database.Integer, nullable=False)
    date_created = database.Column(database.DateTime, default= datetime.now())

    def __init__(self, other_name, surname, email, username, password, birth_date, gender, contact, contact2, address, qualification):
        self.other_name = other_name
        self.email = email
        self.surname = surname
        self.password = generate_password_hash(password)
        self.username = username
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        self.gender = gender
        self.contact = contact
        
    def __repr__(self) -> str: 
        return f"<User: {self.other_name} {self.surname} {self.email} with username {self.username}"
    
    def serializable(self):
        return {
            "other_name" : self.other_name,
            "surname" :self.surname, 
            "email":self.email,
            "username":self.username,
            "birth_date":self.birth_date, 
            "password" : self.password,
            "gender":self.gender,
            "contact":self.contact,
            }
    
    @classmethod
    def add_to_database(cls, user):
        database.session.add(user)
        database.session.commit()


    def update_user(self, surname, other_name, email, password, qualification, contact, contact2, address):
        self.email = email
        self.password = generate_password_hash(password)
        self.surname = surname
        self.other_name = other_name
        self.contact = contact
        database.session.commit()

    @classmethod   
    def delete_user(clc, user):
        database.session.delete(user)
        database.session.commit()

    @classmethod
    def save(cls, user):
        database.session.add(user)
        database.session.commit()