"""
The recipes Blueprint handles the creation, modification, deletion,
and viewing of recipes for this application.
"""
from flask import Blueprint
recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

from . import routes
