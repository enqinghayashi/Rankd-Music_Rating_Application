from flask import session, jsonify
from app import db
from app.models import *
from app.item import Item
from app.api_requests import api

"""
Additional information we want

Tracks: Duration
Albums: Release Date, Total Tracks (Only required for the api analysis)
Artists: Genres

"""

class DatabaseAnalysis:
  def __init__(self, mode):
    self.top_tracks = []
    self.top_albums = []
    self.top_artists = []
    """
    Keys: Minute lengths (i.e. duration_ms//60000)
    Values: (sum of scores, total tracks in this bracket)
    """
    self.length_data = {}
    """
    Keys: Release year
    Values: (sum of scores, total tracks from this year in top_tracks)
    """
    self.release_year_data = {}
    """
    Keys: Genre name
    values: (sum of scores, total tracks in this genre in top_tracks)
    """
    self.genre_data = {}
  def getTopItems(self):
    self.top_tracks = api.getDatabaseItems(search="", type="track")
    self.top_albums = api.getDatabaseItems(search="", type="album")
    self.top_artists = api.getDatabaseItems(search="", type="artist")
  def getTrackLengths(self):
    total_tracks = len(self.top_tracks)
    offset = 0