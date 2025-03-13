from flask import Blueprint
from templates import *
from globals import *

events_bp = Blueprint("events", __name__)

@events_bp.route("/events")
def settings():
    posts = render_template("articles/events.html", articles= "")
    return render_skeleton(f"{app_config["blog-name"]} - Events", posts)