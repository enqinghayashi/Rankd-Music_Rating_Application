from flask import Blueprint

main = Blueprint('main', __name__)

from app import routes  # This will register all routes on the blueprint
