from app import db

from sqlalchemy.schema import PrimaryKeyConstraint

class User(db.Model):
  __table_name__ = 'User'
  
  user_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return 'user_id={}, username={}, email={}, password={}'.format(self.user_id, self.username, self.email, self.password)

class Score(db.Model):
  __table_name__ = 'Score'

  # Score is nullable to allow users to remove their ratings
  score = db.Column(db.Integer, nullable=True)   
  user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
  # From the spotify API
  item_id = db.Column(db.String, primary_key=True)
  item_type = db.Column(db.String, nullable=False)
  title = db.Column(db.String, nullable=False)   
  creator = db.Column(db.String, nullable=False) 
  img_url = db.Column(db.String, nullable=False)

  # Composite Key
  #__table_args__ = (
  #  PrimaryKeyConstraint('user_id', 'item_id')
  #)

  def __repr__(self):
    return 'score={}, title={}, creator={}, item_type={}, img_url={}, user_id={}, item_id={}\
      '.format(self.score, self.title, self.creator, self.item_type, self.img_url, self.user_id, self.item_id)
  