import bcrypt
from db import Connection

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, URLField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email


db = Connection()

class User:
    collection = db.get_collection('users')

    def __init__(self, full_name, username, email, password, bio="", links={}, profile_pic="", banner_img=""):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.links = links
        self.profile_pic = profile_pic
        self.banner_img = banner_img

    def save(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())  # Hash password
        self.collection.insert_one(self.__dict__)
        return "User created successfully"

    @classmethod
    def find_by_username(cls, username):
        return cls.collection.find_one({'username': username})
    
    def find_by_email(cls, email):
        return cls.collection.find_one({'email': email})
    
    @classmethod
    def find_by_id(cls, uid):
        return cls.collection.find_one({'_id': uid})

    @classmethod
    def find_all_users(cls):
        return [user for user in cls.collection.find()]

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])
    bio = StringField('Bio', validators=[Length(max=150)])

class Post:
    collection = db.get_collection('posts')

    def __init__(self, user_id, post_type, cover_img="", thumbnail="",  content={}, caption="", link="", link_text=""):
        self.user_id = user_id
        self.post_type = post_type
        self.cover_img = cover_img
        self.thumbnail = thumbnail
        self.content = content
        self.caption = caption
        self.link = link
        self.link_text = link_text

    def save(self):
        self.collection.insert_one(self.__dict__)

    @classmethod
    def find_by_id(cls, post_id):
        return cls.collection.find_one({'_id': post_id})
