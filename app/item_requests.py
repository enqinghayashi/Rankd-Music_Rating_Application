from flask import session
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api

def getScoreItems(search, type, saved):
  # search database
  #user_id = session["user"]["id"]
  #db_rows = db.session.execute(db.select(Score).filter_by(user_id=user_id)).all()
  #db_items = []
  #for row in db_rows:
  #  db_items.append(Item(row._asdict()))
  #print(db_items)

  # Make search request
  search_items = []
  if not saved:
    search_items = api.search(search, type)