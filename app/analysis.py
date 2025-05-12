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
    self.track_stats = {}

    self.compared_albums = {}
    self.common_albums = {}
    self.album_stats = {}

    self.compared_artists = {}
    self.common_artists = {}
    self.artist_stats = {}

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
        item["difference"] = item["x"] - item["y"]
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
  def calculateLinearRegression(data):
    x = []
    y = []
    ids = list(data.keys())
    for id in ids:
      item = data[id]
      x.append(item["x"])
      y.append(item["y"])
    if x == []:
      raise ValueError
    slope, intercept, correlation_coefficient, p, std_err = stats.linregress(x, y)
    return correlation_coefficient, slope, intercept

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

  """
  """
  @staticmethod
  def analyseItems(setA, setB):
    compared = StatsAnalyser.compareDatasets(setA, setB)
    common = StatsAnalyser.getCommonItems(compared)
    item_stats = {
      "correlation": None,
      "high_high": None,
      "low_low": None,
      "high_low": None,
      "low_high": None,
      "outliers": None
    }

    if (common == {}):
      return compared, common, item_stats
    
    # Correlation
    correlation, slope, intercept =  StatsAnalyser.calculateLinearRegression(common)
    item_stats["correlation"] = correlation
      
    # Outliers
    StatsAnalyser.calculateDistanceFromRegression(common, slope, intercept)
    items = list(common.items())
    items.sort(key=lambda item: item[1]["distance"])
    item_stats["outlier"] = items[0]

    # Extremes

    # This method is commented out because the high_low often produces the same as high_high
    # and to appear more interested we used a different method

    #items.sort(key=lambda item: item[1]["difference"])
    #item_stats["high_low"] = items[0] # largest +ve diff is high rank but low listening
    #print(f"HL {item_stats["high_low"]}")
    #item_stats["low_high"] = items[-1] # largest -ve diff is low rank but high listening
    #print(f"LH {item_stats["low_high"]}")


    # YES I KNOW THIS IS A TERRIBLE WAY OF DOING THIS BUT I DONT HAVE THE TIME TO DO IT BETTER RIGHT NOW
    items.sort(key=lambda item: float(item[1]["x"]))
    max_x = items[-1][1]["x"]
    items.sort(key=lambda item: float(item[1]["y"]))
    max_y = items[-1][1]["y"]
    
    # distance from top right corner
    items.sort(key=lambda item: math.sqrt( (max_x-item[1]["x"])**2 + (max_y-item[1]["y"])**2 ) )
    item_stats["high_high"] = items[0]
    #distance from bottom right corner
    items.sort(key=lambda item: math.sqrt( (max_x-item[1]["x"])**2 + (item[1]["y"])**2 ) )
    item_stats["high_low"] = items[0]
    # distance from top left corner
    items.sort(key=lambda item: math.sqrt( (item[1]["x"])**2 + (max_y - item[1]["y"])**2 ) )
    item_stats["low_high"] = items[0]
    # distance from bottom right corner
    items.sort(key=lambda item: math.sqrt( (item[1]["x"])**2 + (item[1]["y"])**2 ) )
    item_stats["low_low"] = items[0]


    print(f"HH: {item_stats['high_high']}")
    print(f"HL: {item_stats['high_low']}")
    print(f"LH: {item_stats['low_high']}")
    print(f"LL: {item_stats['low_low']}")

    return compared, common, item_stats
  
  def analyseTracksAlbumsArtists(self):
    self.compared_tracks, self.common_tracks, self.track_stats\
    = StatsAnalyser.analyseItems(self.db_stats.listened_tracks, self.api_stats.listened_tracks)

    # These bottom two aren't exactly accurate to the db scores but they are calculated from the
    # db score on tracks so close enough for now
    self.compared_albums, self.common_albums, self.album_stats\
    = StatsAnalyser.analyseItems(self.db_stats.listened_albums, self.api_stats.listened_albums)

    self.compared_artists, self.common_artists, self.artist_stats\
    = StatsAnalyser.analyseItems(self.db_stats.listened_artists, self.api_stats.listened_artists)
    
  """
  """
  def fillInItemsSection(self, analysis):
    self.analyseTracksAlbumsArtists()

    # Get Tracks to display
    display_track_ids = [self.db_stats.top_tracks[0].id, self.api_stats.top_tracks[0].id, self.track_stats["high_high"][0],
                         self.track_stats["high_low"][0], self.track_stats["low_high"][0],\
                         self.track_stats["low_low"][0], self.track_stats["outlier"][0]]
    display_tracks = api.getSeveralItems("tracks", display_track_ids)

    try: # if no common scores the bottom 5 will fail
      analysis["tracks"]["db_top"] = display_tracks[0]
      analysis["tracks"]["api_top"] = display_tracks[1]
      analysis["tracks"]["high_high"] = display_tracks[2]
      analysis["tracks"]["high_low"] = display_tracks[3]
      analysis["tracks"]["low_high"] = display_tracks[4]
      analysis["tracks"]["low_low"] = display_tracks[5]
      analysis["tracks"]["outlier"] = display_tracks[6]
    except:
      pass
    
    analysis["tracks"]["correlation"] = self.track_stats["correlation"]

    # Get Albums to display
    api_top_albums = list(self.api_stats.listened_albums.items())
    api_top_albums.sort(key=lambda album: album[1]["score"])
    api_top_album_id = api_top_albums[0][0]

    display_album_ids = [self.db_stats.top_albums[0].id, api_top_album_id, self.album_stats["high_high"][0],
                         self.album_stats["high_low"][0], self.album_stats["low_high"][0],\
                         self.album_stats["low_low"][0], self.album_stats["outlier"][0]]
    display_albums = api.getSeveralItems("albums", display_album_ids)

    try: # if no common scores the bottom 5 will fail
      analysis["albums"]["db_top"] = display_albums[0]
      analysis["albums"]["api_top"] = display_albums[1]
      analysis["albums"]["high_high"] = display_albums[2]
      analysis["albums"]["high_low"] = display_albums[3]
      analysis["albums"]["low_high"] = display_albums[4]
      analysis["albums"]["low_low"] = display_albums[5]
      analysis["albums"]["outlier"] = display_albums[6]
    except:
      pass

    analysis["albums"]["correlation"] = self.album_stats["correlation"]
    
    # Get Artists to display
    display_artist_ids = [self.db_stats.top_artists[0].id, self.api_stats.top_artists[0].id, self.artist_stats["high_high"][0],
                         self.artist_stats["high_low"][0], self.artist_stats["low_high"][0],\
                         self.artist_stats["low_low"][0], self.artist_stats["outlier"][0]]
    display_artists = api.getSeveralItems("artists", display_artist_ids)

    try: # if no common scores the bottom 5 will fail
      analysis["artists"]["db_top"] = display_artists[0]
      analysis["artists"]["api_top"] = display_artists[1]
      analysis["artists"]["high_high"] = display_artists[2]
      analysis["artists"]["high_low"] = display_artists[3]
      analysis["artists"]["low_high"] = display_artists[4]
      analysis["artists"]["low_low"] = display_artists[5]
      analysis["artists"]["outlier"] = display_artists[6]
    except:
      pass
  
    analysis["artists"]["correlation"] = self.artist_stats["correlation"]

  @staticmethod
  def addAveragesToAggregateData(data):
    output = []
    datafields = list(data.keys())
    for field in datafields:
      item = data[field]
      item["average"] = item["score"]/item["tracks"]
      output.append((field, round(item["average"], 2), 0, 10)) # for graphing
    return output
  
  """
  """
  def fillInGraphsSection(self, analysis):
    titles = ["Track Length (Minutes) by Average Rating Score", "Track Length (Minutes) by Average Listening Score",\
              "Years by Average Rating Score", "Years by Average Listening Score",\
              "Genres by Average Rating Score", "Genres by Average Listening Score"]
    datasets = [self.db_stats.minute_data, self.api_stats.minute_data, self.db_stats.release_year_data,\
                self.api_stats.release_year_data, self.db_stats.genre_data, self.api_stats.genre_data]
    total_datasets = len(datasets)
    for i in range(total_datasets):
      graph_data = StatsAnalyser.addAveragesToAggregateData(datasets[i])
      graph_data.sort(key=lambda item: item[0])
      graph = {
        "title": titles[i],
        "data": graph_data
      }
      analysis["graphs"].append(graph)
  
  """
  """
  def completeAnalysis(self):
    # this is what we are going to fill in and return
    analysis = {
      "tracks": {
        "db_top": None,
        "api_top": None,
        "correlation": None,
        "high_high": None,
        "high_low": None,
        "low_high": None,
        "low_low": None,
        "outlier": None
      },
      "albums": {
        "db_top": None,
        "api_top": None,
        "correlation": None,
        "high_high": None,
        "high_low": None,
        "low_high": None,
        "low_low": None,
        "outlier": None,
      },
      "artists": {
        "db_top": None,
        "api_top": None,
        "correlation": None,
        "high_high": None,
        "high_low": None,
        "low_high": None,
        "low_low": None,
        "outlier": None
      },
      "graphs": []
    }
    self.fillInItemsSection(analysis)
    self.fillInGraphsSection(analysis)
    return analysis