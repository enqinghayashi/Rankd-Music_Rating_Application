from flask import session, jsonify
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api
from app.item_requests import *

"""
REMEMBER TO CHANGE LIMIT ON GETALLTOPITEMS IN API REQUESTS BACK TO 1000 OR WHATEVER FEELS REASONABLE
"""

"""
"""
class AnalysisStats:
  def __init__(self):
    self.top_tracks = []
    self.top_artists = []

    self.top_albums = []

    """
    The following fields have some key that is relevant to the data they represent 
    e.g. id, release year, etc.
    
    The values of these keys always include "score" for total score of items that fall into that
    bracket (e.g. tracks released in 2004), and a "tracks" for the total tracks that fit in the
    bracket.

    Listened albums and artists have a few extra fields that are used to fill in the other data sets.
    """
    self.listened_tracks = {} # useful for comparison between database and api
    self.listened_albums = {} # used for release date analysis
    self.listened_artists = {} # used for genre analysis
    
    self.minute_data = {}
    self.duration_data = {} # finer version of the above, better for analysis
    self.release_year_data = {}
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
  def addScore(self, dataset, bracket, score, tracks):
    try:
      dataset[bracket]
    except KeyError:
      dataset[bracket] = {
        "score": 0,
        "tracks": 0
      }
    dataset[bracket]["score"] += score
    dataset[bracket]["tracks"] += tracks 

  """
  """
  def calculateListenedItems(self):
    for track in self.top_tracks:
      self.addScore(self.listened_tracks, track.id, track.score, 1)
      self.addScore(self.listened_albums, track.album_id, track.score, 1)
      artist_ids = track.artist_ids
      for id in artist_ids:
        self.addScore(self.listened_artists, id, track.score, 1)

  """
  """
  def getTrackData(self):
    track_ids = list(self.listened_tracks.keys())
    track_data = self.getAllItemsData("tracks", track_ids)
    for track in track_data:
      id = track["id"]
      self.listened_tracks[id]["duration_ms"] = track["duration_ms"]
      self.listened_tracks[id]["popularity"] = track["popularity"]
      self.listened_tracks[id]["item"] = Item(track)
  
  """
  """
  def getListenedAlbumData(self):
    album_ids = list(self.listened_albums.keys())
    album_data = self.getAllItemsData("albums", album_ids)
    for album in album_data:
      id = album["id"]
      self.listened_albums[id]["release_year"] = album["release_date"][0:4]
      self.listened_albums[id]["total_tracks"] = album["total_tracks"]
      self.listened_albums[id]["item"] = Item(album)

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
      self.listened_artists[id]["item"] = Item(artist)
  """
  """
  def getBonusData(self):
    self.getTrackData()
    self.getListenedAlbumData()
    self.getListenedArtistData()
  
  """
  """
  def calculateFieldScores(self):
    self.getBonusData()
    
    for track in list(self.listened_tracks.values()):
      minutes = track["duration_ms"]//(60*1000)
      self.addScore(self.minute_data, minutes, track["score"], 1)
      self.addScore(self.duration_data, track["duration_ms"], track["score"], 1)
    
    for album in list(self.listened_albums.values()):
      self.addScore(self.release_year_data, album["release_year"], album["score"], album["tracks"])

    for artist in list(self.listened_artists.values()):
      for genre in artist["genres"]:
        self.addScore(self.genre_data, genre, artist["score"], artist["tracks"])
  
  """
  To be implemented by child class.

  Must fill in top_tracks, top_artists run calculateListenedAlbumsAndArtists()
  """
  def setup(self):
    pass

  """
  """
  def run(self):
    self.setup()
    self.calculateFieldScores()

"""
"""
class DatabaseStats(AnalysisStats):
  def __init__(self):
    super().__init__()
  
  """
  Get user's scores from the database.
  """
  def getTopItemsFromDatabase(self):
    # getDatabaseItems returns a tuple but here we only care about the first item
    self.top_tracks = getDatabaseItems(search="", type="track")
    self.top_albums = getDatabaseItems(search="", type="album")
    self.top_artists = getDatabaseItems(search="", type="artist")
  
  def setup(self):
    self.getTopItemsFromDatabase()
    self.calculateListenedItems()

"""
"""
class APIStats(AnalysisStats):
  def __init__(self):
    super().__init__()
  
  """
  Get users's top tracks and artists from API
  """
  def getTopItemsFromAPI(self):
    self.top_tracks = api.getAllTopItems("tracks")
    self.top_artists = api.getAllTopItems("artists")
  
  """
  """
  def convertPlacementsToScores(self, items):
    total_items = len(items)
    item_weight = 10/(total_items - 1)
    for i in range(total_items):
      items[i].score = 10 - (i * item_weight)
  
  def setup(self):
    self.getTopItemsFromAPI()
    self.convertPlacementsToScores(self.top_tracks)
    self.convertPlacementsToScores(self.top_artists)
    self.calculateListenedItems()