from app import db
from flask_login import UserMixin
from sqlalchemy.schema import PrimaryKeyConstraint

class User(db.Model, UserMixin):
  __table_name__ = 'User'
  
  user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)
  img_url = db.Column(db.String, nullable=False, default='img/profile_pictures/default.png')
  bio = db.Column(db.Text)
  name = db.Column(db.String)
  refresh_token = db.Column(db.String)
  def __repr__(self):
    return 'user_id={}, username={}, email={}, password={} img_url={} , bio = {}, name = {}'.format(self.user_id, self.username, self.email, self.password, self.img_url, self.bio, self.name, self.refresh_token)

  def get_id(self):
    return str(self.user_id)

class Score(db.Model):
  __table_name__ = 'Score'

  score = db.Column(db.Integer, nullable=True) # nullable to allow users to remove their ratings
  user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
  # From the spotify API
  item_id = db.Column(db.String, primary_key=True)
  item_type = db.Column(db.String, nullable=False)
  title = db.Column(db.String, nullable=False)
  creator = db.Column(db.String, nullable=False) 
  img_url = db.Column(db.String, nullable=False)
  album = db.Column(db.String)
  album_id = db.Column(db.String)
  artist_ids = db.Column(db.String) # This will be a string of ids separated by commas

  # Composite Key
  __table_args__ = (
    db.PrimaryKeyConstraint('user_id', 'item_id'), # comma is necessary as table args must be a tuple
  )

  def __repr__(self):
    return 'score={}, title={}, creator={}, item_type={}, img_url={}, user_id={}, item_id={}\
      '.format(self.score, self.title, self.creator, self.item_type, self.img_url, self.user_id, self.item_id)

class Friend(db.Model):
  __table_name__ = 'Friend'

  user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
  friend_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)

  __table_args__ = (
    db.PrimaryKeyConstraint('user_id', 'friend_id'), # comma is necessary as table args must be a tuple
  )
