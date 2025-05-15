import re
from flask import flash, redirect, url_for
from flask_login import current_user
from app import db
from app.models import *

def validate_password(password, confirm_password=None, route_name=None):

    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!#$%^&*])[A-Za-z\d@!#$%^&*]{8,}$'

    if not re.match(regex, password):
        return "Password must contain at least 1 letter, 1 number, and 1 special character."

    if confirm_password and password != confirm_password:
        return "Confirmed passwords do not match."

    return None 

def validate_username(username):
    username_regex = r'^[a-zA-Z0-9_]{3,100}$'
    if not re.match(username_regex, username):
        return "Invalid username. Use letters, numbers, underscores only."
    return None

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return "Invalid email address"
    return None

def validate_score(score):
    if score == "": return score # Used for deletion
    score = score.strip().split(".")
    length = len(score)
    if (length == 1):
        score = score[0]
        if not score.isnumeric(): raise ValueError("Score contains non-numeric characters.")
        if not (int(score) <= 10): raise ValueError("Score is greater than 10.") # Score is too large
        return str(score)
    elif (length == 2): 
        if not (score[0].isnumeric() and score[1].isnumeric()): raise ValueError("Score contains non-numeric characters.") # Not numeric
        if not (int(score[0]) <= 10): raise ValueError("Score is greater than 10.") # Score is too large
        if (int(score[0]) == 10): return "10" # Cap scores at 10
        score = float(score[0] + "." + score[1])
        score = round(score, 2) # round to 2 dp
        return str(score)
    else:
        raise ValueError("Score contains more than one decimal place.")# More than one decimal

def getFriends():
    my_user_id = int(current_user.user_id)
    friends = (
        db.session.query(User)
        .join(Friend, Friend.friend_id == User.user_id)
        .filter(Friend.user_id == my_user_id, Friend.status == 'ACCEPTED')
        .all()
    )
    return friends

def validateFriend(friend_id):
    friends = getFriends()
    friend_len = len(friends)
    for i in range(friend_len):
      if int(friends[i].user_id) == int(friend_id):
        return i
    return -1

def validateDepth(depth):
    if depth not in ("100", "250", "500", "1000", "All"):
        return False
    return True