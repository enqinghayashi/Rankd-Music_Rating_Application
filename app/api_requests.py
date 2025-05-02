import requests
from app.auth import auth
from app.item import Item

class API:
  def __init__(self):
    self.BASE_URL = "https://api.spotify.com/v1/"
  """
  A general method for making requests to the api.

  THIS METHOD SHOULD ONLY BE CALLED INTERNALLY.
  """
  def api_request(self, endpoint, params={}):
    url = self.BASE_URL + endpoint
    try:
      token = auth.getCurrentToken() # raises an exception if user is not logged in
    except:
      return False
    headers = {
      "Authorization": "Bearer  " + token # The two spaces after Bearer are required for some reason
    }
    res = requests.get(url, params=params, headers=headers)
    # Handle errors
    return res.json()

  """
  THIS NEEDS IMPLEMENTING
  """
  def sanitize_query(self, query):
    return query

  """
  Make a search request to the API with the given query.

  NOTE: The limit applies to each type independently. I.e. a limit of 5 returns 5 tracks, 5 albums, and 5 artists if type is left as default.
  """
  def search(self, query, type="track,album,artist", limit=20, offset=0):
    query = self.sanitize_query(query)
    params = {
      "query": query,
      "offset": offset,
      "limit": limit,
      "type": type
    }
    data = self.api_request("search", params)

    search_items = []
    item_types = type.split(',')
    if "track" in item_types:
      for track in data["tracks"]["items"]:
        search_items.append(Item(track))
    if "album" in item_types:
      for album in data["albums"]["items"]:
        search_items.append(Item(album))
    if "artist" in item_types:
      for artist in data["artists"]["items"]:
        search_items.append(Item(artist))
    return search_items
  
  """
  Get a single item from the API.

  Type is one of track, album, or artist.
  """
  def getItem(self, type, id):
    allowed_types = ["track", "album", "artist"]
    if type not in allowed_types:
      return False
    data = self.api_request(type + "s/" + id)

    if "error" in data.keys():
      return None

    return Item(data)
  
  """
  Get several items of the same type.

  Type is one of tracks, albums, or artists.
  ids is an array of ids.

  Raises an exception on error
  """
  def getSeveralItems(self, type, ids):
    allowed_types = ["tracks", "albums", "artists"]
    if type not in allowed_types:
      raise ValueError("Type is not of allowed types.")
    
    # Enforce maximum request lengths
    if type == "albums" and len(ids) > 20:
      raise ValueError("Cannot request more than 20 album ids at a time.")
    elif type != "albums" and len(ids) > 50:
      raise ValueError("cannot request more than 50 Tracks or Artists at a time.")

    ids_str = ""
    for id in ids:
      ids_str += "," + id
    ids_str = ids_str[1:] # remove first comma
    params = {"ids":ids_str}
    
    data = self.api_request(type, params)

    items = []
    for item in data[type]:
      if item == None: # ids of the wrong type return "None", thus can be skipped
        continue
      items.append(Item(item))
    return items
  
  """
  
  """
  def getTopItems(self, type, offset=0, limit=50):
    allowed_types = ["tracks", "artists"]
    if type not in allowed_types:
      raise ValueError("Type is not of allowed types.")
    
    params = {
      "time_range": "long_term",
      "offset": offset,
      "limit": limit,
    }
    
    data = self.api_request("me/top/" + type, params)
    
    items = []
    for item in data["items"]:
      items.append(Item(item))
    
    return items


api = API()