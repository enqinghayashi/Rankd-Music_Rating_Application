import re
from flask import flash, redirect, url_for

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



