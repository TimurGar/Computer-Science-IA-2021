import binascii
import hashlib
import os
from datetime import datetime
from hashlib import md5

from myapp import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

# Creating User table in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # index for searching by username/email
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # One to many relationship between User and Project
    projects = db.relationship('Project', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):

        # hashing a random sequence with 60 bits: produces 256 bits or 64 hex chars
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode(
            'ascii')
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        password_hash = binascii.hexlify(password_hash)
        hashed_password = (salt + password_hash).decode('ascii')
        self.password_hash = hashed_password


    def check_password(self, provided_password, stored_password):
        # Splitting hashed password into salt, and password itself
        # salt = password[:64]
        # password = password[64:]
        #
        # # Decoding
        # password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
        #                               salt.encode('ascii'), 100000)
        # password_hash = binascii.hexlify(password_hash).decode('ascii')
        # return password_hash

        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

        # return check_password_hash(self.password_hash, password)


        # self.password_hash = generate_password_hash(password)


    # Method for returning an avatar from Gravatar.com
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Project(db.Model):
    __searchable__ = ['name', 'description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    description = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # One to many relationship between User and Project
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # One to many relationship between Project and Item
    items = db.relationship('Item', backref='project', lazy='dynamic')

    def avatar(self, size):
        digest = md5(self.name.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

    def __repr__(self):
        return '<Post {} id {}>'.format(self.name, self.id)

    # def get_id(self):
    #     project_id = Project.query.filter_by(self.id)
    #     return project_id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    description = db.Column(db.String(150))
    model_or_type = db.Column(db.String(50), index=True)
    size = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def avatar(self, size):
        digest = md5(self.name.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)


# Terminal commands for the database
# flask db init -- create a .db file
# flask db migrate -m "The first table for User" -- use if we want to make changes to a structure of the database
# flask db upgrade -- apply the changes
# flask db downgrade -- undo the last migration
# flask db history -- see the migration history
# flask db current -- to find out what is the current migration

# Python console
# Adding a use User from python console
# from app import User
# u = User(username = "Test", email = "test@test")
# u.set_password("qwerty")
# from app import db
# db.session.add(u)
# db.session.commit()
# Query
# all_users = User.query.all()