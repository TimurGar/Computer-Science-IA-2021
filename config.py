import os
# Generates absolute path
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # For full-text search
    WHOOSH_BASE = 'whoosh'

    POSTS_PER_PAGE = 3

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_SERVER') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_SERVER') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['timur14168577@gmail.com']