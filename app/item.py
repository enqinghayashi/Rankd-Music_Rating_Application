from flask import session
from app import db
from app.models import Score

class Item:
  def __init__(self, data, from_db=False):
    """
    List of fields for documentation purposes.
    """
    self.id = "" # The ID of the item, used for API requests
    self.score = "" # User rating from the database if it exists
    
    self.type = "" # track, album, artist
    self.title = "" # Title of the item e.g. My Chemical Romance
    self.creator = "" # String of artists e.g. "ROSE, Bruno Mars", "My Chemical Romance" (same as title for artists)
    self.img_url = "" # Image to display
    
    self.album = "" # Name of album if item is track, empty if album or artist (Mostly used for search)
    self.album_id = "" # If the item is a track, the id of the album it belongs to, otherwise blank
    
    self.artist_ids = [] # The IDs of the artists if item is a track or album
    
    """
    Setting fields.
    """
    if from_db:
      self.init_from_database(data)
      return

    # General fields
    self.id = data["id"]
    user_id = session["user"]["id"]
    # NEED TO HANDLE ERRORS HERE FOR DB QUERY
    #self.score = Score.query.get({"user_id": user_id, "item_id": self.id})
    self.type = data["type"]
    self.title = data["name"]

    # Image fields (and album for tracks)
    if self.type == "track":
      try:
        self.img_url = data["album"]["images"][0]["url"]
      except IndexError: # Some items don't have images
        pass
      self.album = data["album"]["name"]
      self.album_id = data["album"]["id"]
    else: 
      try:
        self.img_url = data["images"][0]["url"]
      except IndexError: # Some items don't have images
        pass
   
    # Artist fields
    if self.type == "track" or self.type == "album":
      for artist in data["artists"]:
        self.artist_ids.append(artist["id"])
        self.creator += artist["name"] + ", "
      self.creator = self.creator[0:(len(self.creator)-2)] # Remove the last ", "
    else:
      self.artist_ids.append(self.id)
      self.creator = self.title
  
  def init_from_database(self, data):
    self.score = data.score
    self.id = data.item_id
    self.type = data.item_type
    self.title = data.title
    self.creator = data.creator
    self.img_url = data.img_url
    self.album = data.album
    self.album_id = data.album_id
    self.artist_ids = data.artist_ids.split(",")

  def to_dict(self):
    return {
      "id": self.id,
      "score": self.score,
      "type": self.type,
      "title": self.title,
      "creator": self.creator,
      "img_url": self.img_url,
      "album": self.album,
      "album_id": self.album_id,
      "artist_ids": self.artist_ids
    }
  @staticmethod
  def stringify_artist_ids(artist_ids):
    string = ""
    for id in artist_ids:
      string += "," + id
    return string[1:]
