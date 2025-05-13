from flask import render_template, request, redirect, url_for, flash, session, current_app, jsonify
from urllib import response
from app import app, db
from app.config import Config
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from app.models import User, Friend, Score
from app.auth import auth, UserNotAuthroizedError, BadRefreshTokenError
from app.util import validate_password, validate_email, validate_score, validate_username
from app.item_requests import *
from urllib.parse import parse_qs
from app.analysis import *
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, ChangeEmailForm, EditProfileForm, FriendForm, DeleteAccountForm
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return render_template("index.html", title="Home")

@app.route('/scores', methods=["GET", "POST"])
@login_required
def scores():
  # Alter Database
  if request.method == "POST":
    data = request.json
    user_id = current_user.user_id
    
    try:
       score = validate_score(data["score"])
    except ValueError as e:
       return "Unable to save score. " + str(e)
    
    db_score = db.session.execute(db.select(Score).filter_by(user_id=user_id, item_id=data["id"])).all()
    if db_score != []:
       db_score = Score.query.get({
          "user_id": user_id,
          "item_id": data["id"]
       })

    # remove score from database
    if score == "":
       if db_score == []:
        return "Nothing to delete."
       else:
        db.session.delete(db_score)
        db.session.commit()
        return "Score deleted."
    
    new_score = Score(
      score = score,
      user_id = user_id,
      item_id = data["id"],
      item_type = data["type"],
      title = data["title"],
      creator = data["creator"],
      img_url = data["img_url"],
      album = data["album"],
      album_id = data["album_id"],
      artist_ids = Item.stringify_artist_ids(data["artist_ids"])
    )

    if db_score == []:
      db.session.add(new_score)
    else:
      db_score.score = new_score.score
    db.session.commit()
    
    return "Saved successfully."
  
  # Make Search
  if request.is_json:
    search = request.args.get("search")
    type = request.args.get("type")
    saved = request.args.get("saved")
    response = getScoreItems(search, type, saved)
    return jsonify(response)
  
  # View Page
  return render_template("scores.html", title="Scores")

@app.route('/stats')
@login_required
def stats():

  analysis = StatsAnalyser.getAnalysisFromDB()
  if analysis is None:
    analysis = StatsAnalyser().completeAnalysis()
  
  return render_template("stats.html", title="Stats", analysis=analysis)

@app.route('/compare_scores')
@login_required
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
@login_required
def compare_stats():
  return render_template("compare_stats.html",\
                         title="Compare Stats",\
                         item_comparisons=item_comparisons,\
                         outlier_comparisons=outlier_comparisons,\
                         graphs=graphs,\
                         similarity_percentage=65\
  )

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        if not validate_password(form.password.data):
          password = form.password.data
          hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
          new_user = User(username=username, email=email, password=hashed_password)
          db.session.add(new_user)
          db.session.commit()
          flash("Account created successfully", "success")
          return redirect(url_for('login'))
        elif request.method == 'POST':
          flash("Failed to register. Please check your input.", "danger")
    return render_template("register.html", title="Register", form=form)

@app.route('/validate_user', methods=['POST'])
def validate_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')

    response = {}

    if username:
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            response['username'] = "Username is already taken."
        elif validate_username(username):
            response["username"] = "Invalid username. Use letters, numbers, underscores only."
        else:   
            response['username'] = "Username is available."

    if email:
        existing_email = User.query.filter_by(email=email).first()
        if validate_email(email):
            response['email'] = "Invalid email address. Please enter a valid email."
        elif existing_email:
            response['email'] = "Email is already registered with another account."
        else:
            response['email'] = "Email is available."

    if password is not None and confirm_password is not None:
        validation_error = validate_password(password, confirm_password)
        if validation_error:
            response['password'] = validation_error
        else:
            response['password'] = "Password is valid."

    return response

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect username or password", "danger")
            return redirect(url_for('login'))
        login_user(user)
        flash("Log in successfully", "success")
        try:
            print("DEBUG: Attempting to get current token")
            auth.getCurrentToken()
            print(f"DEBUG: Current token restored")
        except:
            return redirect(url_for('link_to_spotify'))
        return redirect(url_for('index'))
    return render_template("login.html", title="Login", form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user    
    return render_template("profile.html", title="Profile", user=user)
app.config.from_object(Config)
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        if form.profile_picture.data:
            files = form.profile_picture.data
            old_profile = user.img_url
            if old_profile and old_profile != 'img/profile_pictures/default.png':
                old_profile_path = os.path.join(current_app.root_path, 'static', old_profile)
                if os.path.exists(old_profile_path):
                    os.remove(old_profile_path)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(files.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            files.save(file_path)
            user.img_url = f"img/profile_pictures/{filename}"
        user.name = form.name.data
        user.bio = form.bio.data
        db.session.commit()
        flash("Profile updated", "success")
        return redirect(url_for('profile'))
    return render_template("edit_profile.html", title="Edit Profile", user=user, form=form)

app.secret_key = Config.SECRET_KEY

@app.route('/logout')
@login_required
def logout():
  auth.clear()
  logout_user()
  session.clear()
  flash("Logged out successfully", "info")
  return redirect(url_for('index'))

@app.route('/auth')
@app.route('/authenticate')
@app.route('/authorize')
@app.route('/connect_music', methods=['GET'])
@login_required
def link_to_spotify():
  num_args = len(request.args)
  if (num_args == 0): # First visit
    return redirect(auth.generateAuthURL())
  elif (num_args == 1): # After redirect
    if ('code' in request.args.keys()): # User accepted the authorization
      auth.completeAuth(request.args['code'])
      flash("Authorization successful!", "success")
      return redirect(url_for('scores'))
    elif ('error' in request.args.keys()): # User declined the authorization
      flash("Authorization failed! Please try again.", "danger")
      return redirect(url_for('profile'))
    else: # An invalid argument has been given to the route (i.e. user input on purpose)
      flash("Authorization failed! Please try again.", "danger")
      return redirect(url_for('profile'))
  else: # This page should never receive more than 1 argument
    return "Error"

@app.route('/account_settings')
@login_required
def account_settings():
    form = DeleteAccountForm()
    return render_template("account_settings.html", title="Account Setting", form=form)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = current_user
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data
        if not user or not check_password_hash(user.password, current_password):
            flash("Please enter the correct current password", "danger")
            return redirect(url_for('change_password'))
        validation_error = validate_password(new_password, confirm_new_password)
        if validation_error:
            flash(validation_error, "danger")
            return redirect(url_for('change_password'))
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        db.session.commit()
        flash("Password updated successfully", "success")
        return redirect(url_for('account_settings'))
    elif request.method == 'POST':
        flash("Failed to update password. Please check your input.", "danger")
    return render_template('change_password.html', form=form)

@app.route('/validate_password_change', methods=['POST'])
@login_required
def validate_password_change():
    user = current_user
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    confirm_new_password = request.json.get('confirm_new_password')
    response = {}

    if current_password is not None:
        if not check_password_hash(user.password, current_password):
            response['current_password'] = "Current password is incorrect."
        else:
            response['current_password'] = "Current password is correct."

    if new_password is not None and confirm_new_password is not None:
        validation_error = validate_password(new_password, confirm_new_password)
        if validation_error:
            response['new_password'] = validation_error
        else:
            response['new_password'] = "Password is valid."

    return jsonify(response)

@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    user = current_user
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        if User.query.filter_by(email=new_email).first():
            flash("Email is already registered with another account.", "danger")
            return redirect(url_for('change_email'))
        if validate_email(new_email) is not None:
            flash("Invalid email address. Please enter a valid email.", "danger")
            return redirect(url_for('change_email'))
        user.email = new_email
        db.session.commit()
        flash("Email updated successfully", "success")
        return redirect(url_for('account_settings'))

    elif request.method == 'POST':
        flash("Failed to update email. Please check your input.", "danger")
    return render_template("change_email.html", title="change email", user=user, form=form)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = current_user
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Your account has been deleted. See ya', 'info')
        return redirect(url_for('index'))
    else:
        flash('Your account cannot be delete, please contact admin', 'danger')
        return redirect(url_for('account_settings'))

@app.route('/friends', methods=["GET", "POST"])
@login_required
def friends():
    my_user_id = int(current_user.user_id)
    search_results = []
    searching_friends = ""
    search_friend_id = ""
    form = FriendForm()
    # Only show accepted friends
    friends = (
        db.session.query(User)
        .join(Friend, Friend.friend_id == User.user_id)
        .filter(Friend.user_id == my_user_id, Friend.status == 'ACCEPTED')
        .all()
    )
    # Pending requests sent to current user
    pending_requests = (
        db.session.query(User)
        .join(Friend, Friend.user_id == User.user_id)
        .filter(Friend.friend_id == my_user_id, Friend.status == 'PENDING')
        .all()
    )
    search_someone_in_friendlist = friends

    if form.validate_on_submit():
        search_friend_id = form.search_friend_id.data.strip() if form.search_friend_id.data else ""
        searching_friends = form.searching_friends.data.strip() if form.searching_friends.data else ""
        if form.submit_add.data and search_friend_id:
            user = User.query.filter_by(user_id=search_friend_id).first()
            if user:
                if user.user_id != my_user_id:
                    existing_friendship = Friend.query.filter_by(user_id=my_user_id, friend_id=user.user_id).first()
                    if not existing_friendship:
                        # Create a pending request
                        new_friend = Friend(user_id=my_user_id, friend_id=user.user_id, status='PENDING')
                        db.session.add(new_friend)
                        db.session.commit()
                        flash("Friend request sent!", "success")
                        return redirect(url_for('friends'))
                    elif existing_friendship.status == 'PENDING':
                        flash("Friend request already sent.", "info")
                    elif existing_friendship.status == 'ACCEPTED':
                        flash("You are already friends.", "info")
            else:
                flash("No such user", "warning")
        elif form.submit_search.data and searching_friends:
            search_someone_in_friendlist = []
            for friend in friends:
                lowercase_names = searching_friends.lower()
                friend_name = (friend.name or '').lower()
                friend_username = (friend.username or '').lower()
                if lowercase_names in friend_name or lowercase_names in friend_username:
                    search_someone_in_friendlist.append(friend)
        else:
            search_someone_in_friendlist = friends

    # Accept or reject friend requests
    if request.method == 'POST':
        if 'remove_friend_id' in request.form:
            remove_id = int(request.form.get('remove_friend_id'))
            friend = Friend.query.filter_by(user_id=my_user_id, friend_id=remove_id).first()
            if friend:
                db.session.delete(friend)
                db.session.commit()
                flash("Friend removed.", "info")
            return redirect(url_for('friends'))
        elif 'accept_friend_id' in request.form:
            accept_id = int(request.form.get('accept_friend_id'))
            # Find the pending request sent to me
            friend_request = Friend.query.filter_by(user_id=accept_id, friend_id=my_user_id, status='PENDING').first()
            if friend_request:
                friend_request.status = 'ACCEPTED'
                # Also create reciprocal accepted friendship
                reciprocal = Friend.query.filter_by(user_id=my_user_id, friend_id=accept_id).first()
                if not reciprocal:
                    db.session.add(Friend(user_id=my_user_id, friend_id=accept_id, status='ACCEPTED'))
                else:
                    reciprocal.status = 'ACCEPTED'
                db.session.commit()
                flash("Friend request accepted!", "success")
            return redirect(url_for('friends'))
        elif 'reject_friend_id' in request.form:
            reject_id = int(request.form.get('reject_friend_id'))
            friend_request = Friend.query.filter_by(user_id=reject_id, friend_id=my_user_id, status='PENDING').first()
            if friend_request:
                db.session.delete(friend_request)
                db.session.commit()
                flash("Friend request rejected.", "info")
            return redirect(url_for('friends'))

    return render_template(
        'friends.html',
        my_user_id=my_user_id,
        friends=search_someone_in_friendlist,
        search_results=search_results,
        searching_friends=searching_friends,
        search_friend_id=search_friend_id,
        form=form,
        pending_requests=pending_requests
    )