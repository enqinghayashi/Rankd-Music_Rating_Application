from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return render_template("index.html", title="Home")

@app.route('/score')
def score():
  return render_template("score.html", title="Score")