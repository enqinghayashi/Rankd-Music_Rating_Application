import re
from flask import flash, redirect, url_for

def validate_password(password, confirm_password=None, route_name=None):

    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!#$%^&*])[A-Za-z\d@!#$%^&*]{8,}$'

    if not re.match(regex, password):
        flash("Password must contain at least 1 letter, 1 number, and 1 special character.", "error")
        if route_name:
            return redirect(url_for(route_name))

    if len(password) < 8:
        flash("Password must be at least 8 characters long.", "error")
        if route_name:
            return redirect(url_for(route_name))

    if confirm_password and password != confirm_password:
        flash("Confirmed passwords do not match.", "error")
        if route_name:
            return redirect(url_for(route_name))

    return None 