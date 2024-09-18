import bcrypt
import email_validator
from db import Connection

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, URLField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length


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
