from flask import session, jsonify
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api
from app.item_requests import *

"""
Converting position to score:
- Scaling factor = 10/total_items in top tracks
- Score = 10 - position * scaling factor
Most listened to track will be a 10
Least listened to track will be practically a 0
"""

"""
Additional information we want

Tracks: Duration
Albums: Release Date
Artists: Genres

"""

class Analysis:
  def __init__(self):
    """
    Aquired from either database for API
    """
    self.top_tracks = []
    self.top_artists = []

    """
    Can be aquired from the database but must be calculated from the api
    """
    self.top_albums = []

    """
    Keys: relevant (album or artist) id
    Values: (sum of scores, total tracks in this bracket)
            in form {"sum":x, "total":y}
    """
    self.listened_albums = {} # used for release date analysis
    self.listened_artists = {} # used for genre analysis

    """
    Keys: Minute lengths (i.e. duration_ms//60000)
    Values: (sum of scores, total tracks in this bracket)
            in form {"sum":x, "total":y}
    """
    self.duration_data = {}
    
    """
    Keys: Release year
    Values: (sum of scores, total tracks from this year in top_tracks)
            in form {"sum":x, "total":y}
    """
    self.release_year_data = {}
    
    """
    Keys: Genre name
    values: (sum of scores, total tracks in this genre in top_tracks) 
            in form {"sum":x, "total":y}
    """
    self.genre_data = {}
    
  """
  Request the data about the items from the API.
  """
  def getAllItemsData(self, type, ids):
    total = len(ids)
    offset = 0

    max_request = 50
    if type == "albums":
      max_request = 20
    
    data = []
    while offset < total:
      try:
        data += api.getSeveralItems(type, ids[offset:offset+max_request], True)
        offset += max_request
      except IndexError:
        data += api.getSeveralItems(type, ids[offset:], True)
        break
    
    return data

  """
  """
  def addScore(self, dataset, bracket, track):
    try:
      dataset[bracket]
    except KeyError:
      dataset[bracket] = {
        "sum": 0,
        "total": 0
      }
    dataset[bracket]["sum"] += track["score"]
    dataset[bracket]["total"] += 1

  """
  """
  def getTrackIds(self):
    ids = []
    for track in self.top_tracks:
      ids.append(track["id"])
    return ids
  
  """
  """
  def trackAnalysis(self):
    # Get the length of all tracks so we can do length analysis at the same time as getting 
    # album and artist information for release date and genre analysis
    track_ids = self.getTrackIds()
    track_data = self.getAllItemsData("tracks", track_ids)
    
    total_tracks = len(self.top_tracks)
    for i in range(total_tracks):
      duration = track_data[i]["duration_ms"]
      self.top_tracks[i]["duration_ms"] = duration
      
      track = self.top_tracks[i]
      minutes = duration//(60*1000)
      self.addScore(self.duration_data, minutes, track)
      
      self.addScore(self.listened_albums, track["album_id"], track)
      
      artist_ids = track["artist_ids"]
      for id in artist_ids:
        self.addScore(self.listened_artists, id, track)
  
class DatabaseAnalysis(Analysis):
  def __init__(self):
    super().__init__()
  
  """
  Get user's scores from the database.
  """
  def getTopItemsFromDatabase(self):
    self.top_tracks = getDatabaseItems(search="", type="track")[0]
    self.top_albums = getDatabaseItems(search="", type="album")[0]
    self.top_artists = getDatabaseItems(search="", type="artist")[0]
