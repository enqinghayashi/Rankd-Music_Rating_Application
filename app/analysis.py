from flask import session # NEEDS TO BE UPDATED TO FLASK LOGIN
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api
from app.item_requests import *

from scipy import stats
import math

"""
REMEMBER TO CHANGE LIMIT ON GETALLTOPITEMS IN API REQUESTS BACK TO 1000 OR WHATEVER FEELS REASONABLE
"""

#region DataCollection
"""
"""
class AnalysisStats:
  def __init__(self):
    self.top_tracks = []
    self.top_artists = []

    self.top_albums = [] # will be empty for api stats

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
    
    self.duration_data = {} 
    self.minute_data = {} # more broad version of duration data, better for display
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
  def getStats(self):
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
    item_weight = 10/(total_items-1) # top song is a 10, bottom song is a 0
    for i in range(total_items):
      items[i].score = 10 - (i * item_weight)
  
  def setup(self):
    self.getTopItemsFromAPI()
    self.convertPlacementsToScores(self.top_tracks)
    self.convertPlacementsToScores(self.top_artists)
    self.calculateListenedItems()
#endregion

#region Analysis
"""
Performs the analysis on the data found above.
"""
class StatsAnalyser:
  def __init__(self):
    self.db_stats = DatabaseStats()
    self.api_stats = APIStats()
    self.db_stats.getStats()
    self.api_stats.getStats()

    self.compared_tracks = {}
    self.common_tracks = {}
    self.track_stats = {
      "correlation": None,
      "high_high": None,
      "low_low": None,
      "high_low": None,
      "low_high": None,
      "outliers": None
    }

  """
  """
  @staticmethod
  def compareDatasets(setA, setB):
    output = {}
    a_ids = list(setA.keys())
    for id in a_ids:
      output[id] = {
        "x": setA[id]["score"],
        "y": -1,
        "difference": -1,
      }
    
    b_ids = list(setB.keys())
    for id in b_ids:
      try:
        item = output[id]
        item["y"] = setB[id]["score"]
        item["difference"] = abs(item["x"] - item["y"])
      except KeyError:
        output[id] = {
          "x": -1,
          "y": setB[id]["score"],
          "difference": -1,
        }
    return output
  
  """
  """
  @staticmethod
  def getCommonItems(setIn):
    setOut = {}
    ids = list(setIn.keys())
    for id in ids:
      item = setIn[id]
      if item["x"] >= 0 and item["y"] >= 0:
        setOut[id] = item
    return setOut
  
  """
  """
  @staticmethod
  def calculateLinearRegression(setA, setB):
    compared = StatsAnalyser.compareDatasets(setA, setB)
    common = StatsAnalyser.getCommonItems(compared)
    x = []
    y = []
    common_ids = list(common.keys())
    for id in common_ids:
      item = common[id]
      x.append(item["x"])
      y.append(item["y"])
    slope, intercept, correlation_coefficient, p, std_err = stats.linregress(x, y)
    return compared, common, correlation_coefficient, slope, intercept

  """
  Calculate the minimum distance of a point from the line of linear regression.
  """
  @staticmethod
  def calculateDistanceFromRegression(common, reg_slope, reg_intercept):
    if common == {}:
      raise ValueError
    slope = -1/reg_slope #get the perpendicular slope to the regression line
    common_ids = list(common.keys())
    for id in common_ids:
      intercept = common[id]["y"]
      x = (reg_intercept - intercept)/(slope - reg_slope)
      y = slope * x + intercept
      dx = common[id]["x"] - x
      dy = common[id]["y"] - y
      common[id]["distance"] = math.sqrt(dx**2 + dy**2)
  
  @staticmethod
  def sort_by_distance(item):
    return item[1]["distance"]
  
  """
  """
  def analyseTracks(self):
    compared, common, correlation, slope, intercept =\
        StatsAnalyser.calculateLinearRegression(self.db_stats.listened_tracks, self.api_stats.listened_tracks)
    self.compared_tracks = compared
    self.common_tracks = common
    self.track_stats["correlation"] = correlation
    
    # Outlier
    try:
      StatsAnalyser.calculateDistanceFromRegression(self.common_tracks, slope, intercept)
      items = list(self.common_tracks.items())
      items.sort(key=StatsAnalyser.sort_by_distance)
      self.track_stats["outliers"] = items.copy()
    except ValueError:
      pass
    