from flask import session, jsonify
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api
import re

def getScoreItems(search, type, saved):
  # Get user's saved scores
  user_id = session["user"]["id"]
  db_rows = db.session.execute(db.select(Score).filter_by(user_id=user_id, item_type=type).order_by(Score.score)).all()
  db_items = []
  for row in db_rows:
    db_items.append(Item(row[0], True))
  
  # Filter the saved scores to the search
  filtered_items = []
  for item in db_items:
    title = re.search(search, item.title)
    album = re.search(search, item.album)
    creator = re.search(search, item.creator)
    if (title or album or creator): filtered_items.append(item)
  db_items = filtered_items
  
  # Convert items to dictionaries to conver to json to send
  db_ids = []
  total = len(db_items)
  for i in range(0, total):
    db_items[i] = db_items[i].to_dict()
    db_ids.append(db_items[i]["id"])

  # Make search request
  search_items = []
  if saved == "false" and search != "": # This is from a json response
    search_items = api.search(search, type)
  
  # Convert items to dictionaries to conver to json to send
  total = len(search_items)
  for i in range(0, total):
    search_items[i] = search_items[i].to_dict()
    try:
      db_id = db_ids.index(search_items[i]["id"])
      search_items[i]["score"] = db_items[db_id]["score"]
    except ValueError:
      continue
  
  items = {
    "search_results": search_items,
    "db_results": db_items
  }

  return items