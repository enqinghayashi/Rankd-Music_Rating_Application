import requests
from app.auth import auth

class API:
  def __init__(self):
    self.BASE_URL = "https://api.spotify.com/v1/"
  """
  A general method for making requests to the api.

  THIS METHOD SHOULD ONLY BE CALLED INTERNALLY.
  """
  def api_request(self, endpoint, params):
    url = self.BASE_URL + endpoint
    try:
      token = auth.getCurrentToken() # raises an exception if user is not logged in
    except:
      return False
    headers = {
      "Authorization": "Bearer  " + token # The two spaces after Bearer are required for some reason
    }
    res = requests.get(url, params=params, headers=headers)
    return res

  """
  THIS NEEDS IMPLEMENTING
  """
  def sanitize_query(self, query):
    return query

  """
  Make a search request to the API with the given query.

  NOTE: The limit applies to each type independently. I.e. a limit of 5 returns 5 tracks, 5 albums, and 5 artists if type is left as default.
  """
  def search(self, query, offset=0, limit=5, type="track,album,artist"):
    query = self.sanitize_query(query)
    params = {
      "query": query,
      "offset": offset,
      "limit": limit,
      "type": type
    }
    response = self.api_request("search", params)
    data = response.json()
    return data

api = API()