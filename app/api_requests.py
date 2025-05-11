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
          token = auth.getCurrentToken() # check if user linked to spotify
      except Exception as e:
          print("Token error:", e) # returns error if not
          return False
      headers = {
          "Authorization": "Bearer  " + token
      }
      res = requests.get(url, params=params, headers=headers)
      
      # check the response from Spotify API before doing any conversions
      try:
          res.raise_for_status()
      except Exception as e:
          print(f"Spotify API error: {e}")
          print(f"Status code: {res.status_code}")
          print(f"Response text: {res.text}")
          return {} 
      
      try:
          return res.json()
      except Exception as e:
          print(f"JSON parse error: {e}")
          print(f"Response text: {res.text}")
          return {}

  """
  THIS NEEDS IMPLEMENTING
  """
  def sanitize_query(self, query):
    return query

  """
  Make a search request to the API with the given query.

  NOTE: The limit applies to each type independently. I.e. a limit of 5 returns 5 tracks, 5 albums, and 5 artists if type is left as default.
  """
  def search(self, query, type, limit=20, offset=0):
      query = self.sanitize_query(query)

      if not query:  # avoid empty query to the API
          return []

      if type not in ["track", "album", "artist"]: 
          type = "track"

      params = {
        "query": query,
        "offset": offset,
        "limit": limit,
        "type": type
      }
      data = self.api_request("search", params)

      search_items = []

      data_key = type + "s"  # tracks, albums, artists
      if data_key in data and "items" in data[data_key]: # check we got the expected keys
          for item in data[data_key]["items"]:
              search_items.append(Item(item))
      else:
          print(f"Spotify response did not include '{data_key}/items' (data was: {data}).")
      # print the errors
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
  def getSeveralItems(self, type, ids, return_data=False):
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
    if return_data:
       return data[type]

    items = []
    for item in data[type]:
      if item == None: # ids of the wrong type return "None", thus can be skipped
        continue
      items.append(Item(item))
    return items
  
  """
  Gets a user's top tracks or artists (max 50 at a time).
  """
  def getTopItems(self, type, offset=0, limit=50):
    # This method should only be called by the getAllTop Items so doesn't need type validation again
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

  """
  Get all of a user's top items up to limit.

  Type can only be track or artist.

  Intended to only be used in the analysis section.
  """
  def getAllTopItems(self, type, limit=1000):
    allowed_types = ["tracks", "artists"]
    if type not in allowed_types:
      raise ValueError("Type is not of allowed types.")
    
    received = 0
    items = []
    while received < limit:
      new_items = self.getTopItems(type, received)
      if new_items == []: # limit was higher than available tracks
        break
      items += new_items
      received += len(new_items)
    return items[:limit]

api = API()