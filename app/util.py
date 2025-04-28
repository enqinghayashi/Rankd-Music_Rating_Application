import re
from flask import flash, redirect, url_for

def validate_password(password, confirm_password=None, route_name=None):

    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!#$%^&*])[A-Za-z\d@!#$%^&*]{8,}$'

    if not re.match(regex, password):
        flash("Password must contain at least 1 letter, 1 number, and 1 special character.", "danger")
        return "Password does not meet the requirement"


    if len(password) < 8:
        flash("Password must be at least 8 characters long.", "danger")
        return "Password is too short"

    if confirm_password and password != confirm_password:
        flash("Confirmed passwords do not match.", "danger")
        return "Password does not match"
    return None 

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        flash("Invalid email address", "danger")
        return "Email address seems fake"
    return None