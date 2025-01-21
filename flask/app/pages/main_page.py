from flask import Blueprint, abort
from templates import *
from globals import *
from articles import *

main_page_bp = Blueprint("main_page", __name__)

@main_page_bp.route("/")
def settings():
    article = render_article(app_config['main-page'], False)
    if article is None:
        return abort(404)
    else:
        return render_skeleton("Carpa", article['article'])