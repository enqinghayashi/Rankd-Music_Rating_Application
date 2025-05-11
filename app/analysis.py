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
  def addScore(self, dataset, bracket, score, total):
    try:
      dataset[bracket]
    except KeyError:
      dataset[bracket] = {
        "sum": 0,
        "total": 0
      }
    dataset[bracket]["sum"] += score
    dataset[bracket]["total"] += total

  """
  """
  def getTrackIds(self):
    ids = []
    for track in self.top_tracks:
      ids.append(track["id"])
    return ids
  
  """
  """
  def calcualteListenedAlbumsAndArtists(self):
    for track in self.top_tracks:
      self.addScore(self.listened_albums, track["album_id"], track["score"], 1)
      artist_ids = track["artist_ids"]
      for id in artist_ids:
        self.addScore(self.listened_artists, id, track["score"], 1)

  """
  """
  def getTrackData(self):
    track_ids = self.getTrackIds()
    track_data = self.getAllItemsData("tracks", track_ids)
    
    total_tracks = len(self.top_tracks)
    for i in range(total_tracks):
      track = self.top_tracks[i]
      track["duration_ms"] = track_data[i]["duration_ms"]
      track["popularity"] = track_data[i]["popularity"]

  """
  """
  def getListenedAlbumData(self):
    album_ids = list(self.listened_albums.keys())
    album_data = self.getAllItemsData("albums", album_ids)
    for album in album_data:
      id = album["id"]
      self.listened_albums[id]["release_year"] = album["release_date"][0:4]
      self.listened_albums[id]["total_tracks"] = album["total_tracks"]

  """
  """
  def getListenedArtistData(self):
    artist_ids = list(self.listened_artists.keys())
    artist_data = self.getAllItemsData("artists", artist_ids)
    for artist in artist_data:
      id = artist["id"]
      self.listened_artists[id]["genres"] = artist["genres"]
      self.listened_artists[id]["popularity"] = artist["popularity"]
      self.listened_artists[id]["followers"] = artist["followers"]["total"]
  
  """
  """
  def getBonusData(self):
    self.getTrackData()
    self.getListenedAlbumData()
    self.getListenedArtistData()

  """
  """
  def durationAnalysis(self):
    for track in self.top_tracks:
      minutes = track["duration_ms"]//(60*1000)
      self.addScore(self.duration_data, minutes, track["score"], 1)

  """
  """
  def releaseYearAnalysis(self):
    pass

  """
  """
  def genreAnalysis(self):
    pass

"""
"""
class DatabaseAnalysis(Analysis):
  def __init__(self):
    super().__init__()
  
  """
  Get user's scores from the database.
  """
  def getTopItemsFromDatabase(self):
    # getDatabaseItems returns a tuple but here we only care about the first item
    self.top_tracks = getDatabaseItems(search="", type="track")[0]
    self.top_albums = getDatabaseItems(search="", type="album")[0]
    self.top_artists = getDatabaseItems(search="", type="artist")[0]

  def run(self):
    self.getTopItemsFromDatabase()
    self.calcualteListenedAlbumsAndArtists()
    self.getBonusData()