from flask import Blueprint, render_template, request
from templates import *
from pages.not_found import not_found

amenities_bp = Blueprint("amenities_pages", __name__)

@amenities_bp.route("/amenity")
def amenity():
    year: str = request.args.get('year')
    weeknum: str = request.args.get('week')
    use_404 = False
    if year is not None or weeknum is not None:
        use_404 = True

    if year is None or not year.isdecimal() or weeknum is None or not weeknum.isdecimal():
        year, weeknum = get_current_week()
    else:
        year = int(year)
        weeknum = int(weeknum)

    amenity = get_amenity(year, weeknum)
    if amenity is not None:
        content = render_template("amenity.html", amenity = amenity)
        return render_skeleton(f"{app_config["blog-name"]} - Amenity", content)
    elif use_404:
        return not_found()
    else:
        content = render_template("amenity.html", amenity = render_template("amenities/origin.html"))
        return render_skeleton(f"{app_config["blog-name"]} - Amenity", content)

def get_amenity(year, weeknum):
    try:
        print(f"/blog/data/amenities/year{year:4}week{weeknum:02}.html")
        with open(f"/blog/data/amenities/year{year:4}week{weeknum:02}.html", "r") as f:
            return f.read()
    except:
        return None

def get_current_week():
    from datetime import datetime

    now = datetime.now()
    year = now.isocalendar()[0]
    weeknum = now.isocalendar()[1]
    return (year, weeknum)