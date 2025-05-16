import os
basedir = os.path.abspath(os.path.dirname(__file__))
default_database_url = 'sqlite:///' + os.path.join(basedir, 'app.db')
class Config(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_database_url
  SECRET_KEY = os.environ.get("SECRET_KEY")
  UPLOAD_FOLDER = 'app/static/img/profile_pictures'
  ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class DeploymentConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_database_url

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'

