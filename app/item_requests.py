from flask import session, jsonify
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api

def getScoreItems(search, type, saved):
  # Get user's saved scores
  user_id = session["user"]["id"]
  db_rows = db.session.execute(db.select(Score).filter_by(user_id=user_id).filter_by(item_type=type)).all()
  db_items = []
  for row in db_rows:
    db_items.append(Item(row._asdict()))
  
  # TODO Filter the saved scores to the search

  # Make search request
  search_items = []
  if saved == "false" and search != "": # This is from a json response
    search_items = api.search(search, type)
  
  items = search_items + db_items # This may have duplicates, that is fine
  
  # Convert items to json to send
  total_items = len(items)
  for i in range(0, total_items):
    items[i] = items[i].to_dict()
  return jsonify(items)