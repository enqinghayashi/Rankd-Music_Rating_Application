from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.config import Config
from werkzeug.utils import secure_filename
import os
from app.auth import auth

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return render_template("index.html", title="Home")

@app.route('/scores')
def scores():
  items = [
    {
      "id": "",
      "type": "track",
      "title": "Welcome To The Black Parade", 
      "creator": "My Chemical Romance", 
      "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      "score": "10"
    },
    {
      "id": "",
      "type": "album",
      "title": "The Black Parade", 
      "creator": "My Chemical Romance", 
      "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      "score": "9.9"
    },
    {
      "id": "",
      "type": "artist",
      "title": "My Chemical Romance", 
      "creator": "My Chemical Romance", 
      "img_url": 'https://i.scdn.co/image/ab6761610000f1789c00ad0308287b38b8fdabc2',
      "score": ""
    }
  ]
  return render_template("scores.html", title="Scores", items=items)

@app.route('/stats')
def stats():
  return render_template("stats.html", title="Stats")

@app.route('/compare_scores')
def compare_scores():
  my_items = [
    {
      "id": "",
      "type": "track",
      "title": "Welcome To The Black Parade", 
      "creator": "My Chemical Romance", 
      "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      "score": "10"
    },
    {
      "id": "",
      "type": "album",
      "title": "The Black Parade", 
      "creator": "My Chemical Romance", 
      "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      "score": "9.9"
    },
    {
      "id": "",
      "type": "artist",
      "title": "My Chemical Romance", 
      "creator": "My Chemical Romance", 
      "img_url": 'https://i.scdn.co/image/ab6761610000f1789c00ad0308287b38b8fdabc2',
      "score": ""
    }
  ]
  friend_items = [
    {
      "id": "",
      "type": "track",
      "title": "Welcome To The Black Parade", 
      "creator": "My Chemical Romance", 
      "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      "score": "9"
    },
    {
      "id": "",
      "type": "album",
      "title": "The Black Parade", 
      "creator": "My Chemical Romance", 
      "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      "score": "8"
    },
    {
      "id": "",
      "type": "artist",
      "title": "My Chemical Romance", 
      "creator": "My Chemical Romance", 
      "img_url": 'https://i.scdn.co/image/ab6761610000f1789c00ad0308287b38b8fdabc2',
      "score": ""
    }
  ]
  return render_template("compare_scores.html", title="Compare Scores", my_items=my_items, friend_items=friend_items)

@app.route('/compare_stats')
def compare_stats():
  return render_template("compare_stats.html", title="Compare Stats")

import re
@app.route('/register', methods=['GET', 'POST'])
def register():
  regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!#$%^&*])[A-Za-z\d@!#$%^&*]{8,}$'
  
  if request.method == 'POST':
    password = request.form['password']
    confirmed_password = request.form['confirm_password']
    if not re.match(regex, password):
        flash("Password must contain at least 1 letter and 1 special character", "error")
        return redirect(url_for('register'))
    if len(password) < 8:
        flash("Password must be at least 8 characters long", "error")
        return redirect(url_for('register'))
    if password != request.form['confirm_password']:
        flash("Passwords do not match", "error")
        return redirect(url_for('register'))
    pass
  return render_template("register.html", title="Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
#    if username == "":
#      flash("Username cannot be empty", "error")
#      return redirect(url_for('login'))
#    if password == "":
#      flash("Password cannot be empty", "error")
#      return redirect(url_for('login'))
#    pass
    if username == "admin" and password == "admin":
      session['user'] = {
        "username": "admin",
        "name": "Admin",
        "bio": "This is a test bio",
        "img_url": "https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1",
      }
      flash("Logged in successfully", "success")
      return redirect(url_for('index'))
    else:
      flash("Invalid username or password", "error")
      return redirect(url_for('login'))
  return render_template("login.html", title="Login")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
  user = session.get('user')
  return render_template("profile.html", title="Profile", user=user)

app.config.from_object(Config)
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
  user = session ['user']
  if request.method == 'POST':
    if 'profile_picture' in request.files:
      files = request.files['profile_picture']
      if files.filename != '':
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filename = secure_filename(files.filename)
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user['img_url'] = f"static/img/profile_pictures/{filename}"
    user['name'] = request.form['name']
    user['bio'] = request.form['bio']
    session['user'] = user
    flash("Profile updated", "success")
    return redirect(url_for('profile'))
  
  return render_template("edit_profile.html", title="Edit Profile", user=user)
  
app.secret_key = Config.SERCRET_KEY
@app.route('/logout')
def logout():
  session.pop('user', None)
  flash("Logged out successfully", "success")
  return redirect(url_for('index'))

@app.route('/auth')
@app.route('/authenticate')
@app.route('/authorize')
def link_to_spotify():
  num_args = len(request.args)
  if (num_args == 0):
    return redirect(auth.generateAuthURL())
  elif (num_args == 1):
    if ('code' in request.args.keys()): # User accepted the authorization
      return "Success"
    elif ('error' in request.args.keys()): # User declined the authorization
      return "Failure"
    else: # An invalid argument has been given to the route
      return "Error"
  else: # This page should never receive more than 1 argument
    return "Error"