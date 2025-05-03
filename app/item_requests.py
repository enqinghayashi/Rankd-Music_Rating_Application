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
  
  # Convert items to json to send
  total = len(db_items)
  for i in range(0, total):
    db_items[i] = db_items[i].to_dict()
  
  total = len(search_items)
  for i in range(0, total):
    search_items[i] = search_items[i].to_dict()
  
  items = {
    "search_results": search_items,
    "db_results": db_items
  }

  return items