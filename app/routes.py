from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.config import Config
from werkzeug.utils import secure_filename
import os
from app.models import User
from app.util import validate_password


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


@app.route('/register', methods=['GET', 'POST'])
def register():
  regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!#$%^&*])[A-Za-z\d@!#$%^&*]{8,}$'
  
  if request.method == 'POST':
    password = request.form['password']
    confirmed_password = request.form['confirm_password']
    validation_error = validate_password(password, confirmed_password)
    if validation_error:
        return validation_error
    flash("Account created successfully", "success")
    return redirect(url_for('login'))
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

@app.route('/account_settings')
def account():
  return render_template("account_settings.html", title = "Account Setting")

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = session.get('users')
    if request.method == 'POST':
        current_password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        if current_password != user['password']:
            flash("Please enter the correct current password", "error")
            return redirect(url_for('change_password'))
        validation_error = validate_password(new_password, confirm_new_password)
        if validation_error:
            return validation_error
        user['password'] = new_password
        session['user'] = user
        flash("Account created successfully", "success")
        return redirect(url_for('index'))
    return render_template('change_password.html')

@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    user = session.get('user')
    if request.method == 'POST':
      user['email'] = request.form['email']
      session['user'] = user
      flash("Email updated successfully", "success")
      return redirect(url_for('account'))
    return render_template("change_email.html", title = "change email", user = user)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    return "Account Deleted"

@app.route('/connect_music', methods=['GET'])
def connect_music():
    return "Connect to your music service page"