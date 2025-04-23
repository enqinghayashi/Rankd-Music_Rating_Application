import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  SERCRET_KEY = 'admin3403'
  UPLOAD_FOLDER = 'app/static/img/profile_pictures'
  ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
