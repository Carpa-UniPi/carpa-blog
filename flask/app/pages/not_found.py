from flask import Blueprint, render_template
from templates import *

not_found_bp = Blueprint("404_page", __name__)

@not_found_bp.errorhandler(404)
def not_found(error = None):
    return render_skeleton("404...", render_template("404.html"))