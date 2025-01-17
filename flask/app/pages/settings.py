from flask import Blueprint, redirect, render_template, request
from templates import *
from globals import *
from session import UserDataUpdateBuilder

settings_bp = Blueprint("settings_page", __name__)

@settings_bp.route("/settings", methods=['GET'])
def settings():
    if not user_management.is_logged_in():
        return redirect("/")

    user = user_management.get_user_data()

    page = render_template("/settings/main.html", checked= user.public)
    return render_skeleton("Settings", page)

@settings_bp.route("/settings", methods=['POST'])
def update_settings():
    if not user_management.is_logged_in():
        return redirect("/")

    set_public = request.form.get('public-account') is not None

    update_builder = UserDataUpdateBuilder()
    update_builder.update_public(set_public)

    user_management.update_user(
        user_management.get_logged_user(),
        update_builder
    )

    return redirect("/settings")