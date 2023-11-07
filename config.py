import os

class Config(object):
  basedir = os.path.abspath(os.path.dirname(__file__)) # You will need line 4, 10 and 11 if you want to use flask migrate and flasksqlalchemy


  FLASK_APP = os.environ.get("FLASK_APP")
  FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
