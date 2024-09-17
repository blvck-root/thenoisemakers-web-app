import bcrypt
import email_validator
from db import Connection

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, URLField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length


db = Connection()
def unique(collection, property):
    """Decorator that checks if a form field is unique in the specified collection.

    Args:
        collection (MotorCollection): The MongoDB collection to check for uniqueness.
        property (str): The property name (e.g., "username", "email") to check for uniqueness.

    Returns:
        callable: A validation function for the form field.
    """
    def validate(form, field):
        if collection.find_one({property: field.data}):
            raise ValidationError(f"User with that {property} already exists")

    return validate

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
    username = StringField('Username', validators=[DataRequired(), unique(User.collection, 'username'), Length(min=4, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email(message="Invalid email address"), unique(User.collection, 'email')])
    password = PasswordField('New Password', validators=[DataRequired()])
    # password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    # confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])
    bio = StringField('Bio', validators=[Length(max=150)])
