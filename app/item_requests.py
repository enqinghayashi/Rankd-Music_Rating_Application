from flask import session, jsonify
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api
import re

def getDatabaseItems(search, type):
  # Get user's saved scores
  user_id = session["user"]["id"]
  db_rows = db.session.execute(db.select(Score).filter_by(user_id=user_id, item_type=type).order_by(Score.score)).all()
  db_items = []
  for row in db_rows:
    db_items.append(Item(row[0], True))
  
  # This is used to add scores to the search results
  # Our filter algorithm and spotify's search are different so this ensure we don't miss anything
  db_ids = []
  total = len(db_items)
  for i in range(0, total):
    db_ids.append(db_items[i].id)

  # Filter the saved scores to the search
  filtered_items = []
  for item in db_items: # I know the filter() method exists but this needs 2 parameters which was annoying to do
    title = re.search(search, item.title)
    album = re.search(search, item.album)
    creator = re.search(search, item.creator)
    if (title or album or creator): filtered_items.append(item)
  
  # Convert items to dictionaries to convert to json to send later
  total = len(filtered_items)
  for i in range(0, total):
    filtered_items[i] = filtered_items[i].to_dict()

  return db_items, db_ids, filtered_items

def getScoreItems(search, type, saved):
  db_items, db_ids, filtered_items = getDatabaseItems(search, type)
  
  # Make search request
  search_items = []
  if saved == "false" and search != "": # This is from a json response
    search_items = api.search(search, type)
  
  # Convert items to dictionaries to convert to json to send later
  total = len(search_items)
  for i in range(0, total):
    search_items[i] = search_items[i].to_dict()
    try: # Add scores of saved items
      db_id = db_ids.index(search_items[i]["id"])
      search_items[i]["score"] = db_items[db_id].score # This is meant to be db_items NOT filtered_items
    except ValueError:
      continue
  
  items = {
    "search_results": search_items,
    "db_results": filtered_items
  }

  return items