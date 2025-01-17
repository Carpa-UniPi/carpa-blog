from flask import Blueprint
from templates import *
from globals import *

main_page_bp = Blueprint("main_page", __name__)

@main_page_bp.route("/")
def settings():
    return render_skeleton("Carpa", "")