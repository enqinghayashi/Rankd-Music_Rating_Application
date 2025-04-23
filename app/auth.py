import random
from Crypto.Hash import SHA256
from base64 import b64encode
from urllib.parse import urlencode
import requests
import datetime

class Auth:
  def __init__(self):
    self.client_id = "45ef5d2726a44fb3b06299adab1fb822"
    self.redirect_uri = "http://127.0.0.1:5000/authenticate"
    self.code_verifier = ""
    self.code_challenge = ""
    self.auth_code = ""
    self.access_token = ""
    self.refresh_token = ""
    self.time_token_granted = ""
  def generateRandomString(self, length):
    available_characters = "ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz0123456789"
    available_characters_length = len(available_characters)
    random_string = ""
    random_int = 0
    for i in range(0,length):
      random_int = random.randint(0, available_characters_length-1)
      random_string += available_characters[random_int]
    return random_string
  def sha256(self, input):
    data = input.encode("utf-8")
    hash = SHA256.new()
    hash.update(data)
    return hash.digest()
  def base64encode(self, input):
    return b64encode(input).decode().replace("=","").replace("+","-").replace("/","_")
  def generateCodeChallenge(self, input):
    hashed = self.sha256(input)
    code_challenge = self.base64encode(hashed)
    return code_challenge
  def generateAuthURL(self):
    self.code_verifier = self.generateRandomString(128)
    self.code_challenge = self.generateCodeChallenge(self.code_verifier)
    url = "https://accounts.spotify.com/authorize"
    params = {
      "client_id": self.client_id,
      "response_type": "code",
      "redirect_uri": self.redirect_uri,
      "scope": "playlist-read-private playlist-read-collaborative user-top-read user-read-recently-played user-library-read",
      "code_challenge_method": "S256",
      "code_challenge": self.code_challenge
    }
    auth_url = url + "?" + urlencode(params)
    return auth_url
  def requestAccessToken(self):
    url = "https://accounts.spotify.com/api/token"
    headers = {
      "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
      "grant_type": "authorization_code",
      "code": self.auth_code,
      "redirect_uri": self.redirect_uri,
      "client_id": self.client_id,
      "code_verifier": self.code_verifier
    }
    return requests.post(url, headers=headers, data=data)
  
auth = Auth()