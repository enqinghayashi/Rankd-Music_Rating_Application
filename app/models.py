from app import db

from sqlalchemy.schema import PrimaryKeyConstraint

class User(db.Model):
  __table_name__ = 'User'
  
  user_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  username = db.Column(db.String, unique = True, nullable=False)
  email = db.Column(db.String, unique = True, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return 'user_id={}, username={}, email={}, password={}'.format(self.user_id, self.username, self.email, self.password)

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
