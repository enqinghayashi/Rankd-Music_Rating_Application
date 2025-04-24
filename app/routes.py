from flask import render_template, request, redirect, url_for, flash, session
from urllib import response
from app import app, db
from app.config import Config
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from app.auth import auth
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
  
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirmed_password = request.form['confirm_password']
    validation_error = validate_password(password, confirmed_password)
    if validation_error:
        return validation_error

    hashed_password = generate_password_hash(password, method = 'pbkdf2:sha256')
    new_user = User(username=username, email=email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash("Account created successfully", "success")
    return redirect(url_for('login'))
  return render_template("register.html", title="Register")

@app.route('/validate_user', methods=['POST'])
def validate_user():
    username = request.json.get('username')
    email = request.json.get('email')

    response = {}

    if username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            response['username'] = "Username is already taken."
        else:
            response['username'] = "Username is available."

    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            response['email'] = "Email is already registered with another account."
        else:
            response['email'] = "Email is available."

    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user:
      flash("User does not exist", "error")
      return redirect(url_for('login'))
    if not check_password_hash(user.password, password):
      flash("Incorrect password", "error")
      return redirect(url_for('login'))
    session['user'] = {'id': user.user_id, 'username': user.username, 'email': user.email}
    flash(f"Log in successfully", "success")
    return redirect(url_for('index'))
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
    user_id = session['user']['id']
    user = User.query.get(user_id)  
    if request.method == 'POST':
      if 'profile_picture' in request.files:
        files = request.files['profile_picture']
        if files.filename != '':
          if not os.path.exists(app.config['UPLOAD_FOLDER']):
              os.makedirs(app.config['UPLOAD_FOLDER'])
          filename = secure_filename(files.filename)
          file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          files.save(file_path)
          user.img_url = f"static/img/profile_pictures/{filename}"
      user.name = request.form['name']
      user.bio = request.form['bio']
      db.session.commit()
      flash("Profile updated", "success")
      return redirect(url_for('profile'))
  
    return render_template("edit_profile.html", title="Edit Profile", user=user)

app.secret_key = Config.SECRET_KEY

@app.route('/logout')
def logout():
  session.pop('user', None)
  flash("Logged out successfully", "success")
  return redirect(url_for('index'))

@app.route('/auth')
@app.route('/authenticate')
@app.route('/authorize')
@app.route('/connect_music', methods=['GET'])
def link_to_spotify():
  num_args = len(request.args)
  if (num_args == 0): # First visit
    return redirect(auth.generateAuthURL())
  elif (num_args == 1): # After redirect
    if ('code' in request.args.keys()): # User accepted the authorization
      auth.completeAuth(request.args['code'])
      return "Success!"
    elif ('error' in request.args.keys()): # User declined the authorization
      return "Failure"
    else: # An invalid argument has been given to the route (i.e. user input on purpose)
      return "Error"
  else: # This page should never receive more than 1 argument
    return "Error"

@app.route('/account_settings')
def account_settings():
  return render_template("account_settings.html", title = "Account Setting")

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user_id = session['user']['id']
    user = User.query.get(user_id)
    if request.method == 'POST':
        current_password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        if not user or not check_password_hash(user.password, current_password):
            flash("Please enter the correct current password", "error")
            return redirect(url_for('change_password'))
        validation_error = validate_password(new_password, confirm_new_password)
        if validation_error:
            return validation_error
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        flash("Password updated successfully", "success")
        return redirect(url_for('account_settings'))
    return render_template('change_password.html')

@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    user_id = session['user']['id']
    user = User.query.get(user_id)
    if request.method == 'POST':
      new_email = request.form['email']
      if User.query.filter_by(email=new_email).first():
            flash("This email is already in use. Please enter a different one", "danger")
      else:
            user.email = new_email
            db.session.commit()
            session['user']['email'] = new_email
            flash("Email updated successfully", "success")
      return redirect(url_for('account_settings'))
    return render_template("change_email.html", title = "change email", user = user)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    return "Account Deleted"
