import random
from Crypto.Hash import SHA256
import base64

class Auth:
  def __init__(self):
    self.client_id = "45ef5d2726a44fb3b06299adab1fb822"
    self.redirect_uri = "https://localhost:5000/authenticate"
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
    return base64.b64encode(input).decode().replace("=","").replace("+","-").replace("/","_")
  def generateCodeChallenge(self, input):
    hashed = self.sha256(input)
    code_challenge = self.base64encode(hashed)
    return code_challenge
    
auth = Auth()