import random
from Crypto.Hash import SHA256

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
    hash_hex = hash.hexdigest()
    return hash_hex
  def base64encode(self, input):
    pass
  def generateCodeChallenge(self, input):
    hashed = self.sha256(input)
    code_challenge = self.base64encode(hashed)
    return code_challenge
    
test_input = "chMtyufB7X7MROVVAa3rt9yHhYKRDtMovjFwNxe02LWfvxyouNpufwIrgBGM1BOdUCpkCQaTYUSofahKcpQdMcsKGn01w6HLSMHPW8yH6m16oILQP6689OyGe6fXlJRQ"
expected_code_challenge = "PYbYtoexwDw6wzWLcHtPZxF2Sh_exu6rKOoUljNJvBM"
auth = Auth()