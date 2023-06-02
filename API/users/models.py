from API.extensions import database
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(database.Model):
    __tablename__ = "USER"
    public_id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=True)
    contact = database.Column(database.Integer, nullable=False)
    date_created = database.Column(database.DateTime, default= datetime.now())

    def __init__(self,email, username, password, contact):
        self.email = email
        self.password = generate_password_hash(password)
        self.username = username
        self.contact = contact
        
    def __repr__(self) -> str: 
        return f"<User: {self.email} with username {self.username}"
    
    def serializable(self):
        return {
            "email":self.email,
            "username":self.username,
            "password" : self.password,
            "contact":self.contact,
            }
    
    @classmethod
    def add_to_database(cls, user):
        database.session.add(user)
        database.session.commit()


    def update_user(self, email, password, contact):
        self.email = email
        self.password = generate_password_hash(password)
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