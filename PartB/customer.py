from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import smtplib
import ssl
import os

customerbp = Blueprint("customerbp", __name__, template_folder="templates")
#PEOPLE_FOLDER = os.path.join('static', 'people_photo')
@customerbp.route("/", methods=["GET"])
def user():
    """
    Routing to customer's page
    """
    if ("user" in session) and (session["position"] == "customer"):
        user = session["user"]
        return render_template("booking.html", user = user)
    else:
        return redirect(url_for("login"))
@customerbp.route("/contact", methods=["GET"])
def customerContact():
    """
    Routing to customer's page
    """
    if ("user" in session) and (session["position"] == "customer"):
        return render_template("contactus.html")
    else:
        return redirect(url_for("login"))

from flask_login import login_user

...
@customerbp.route('/login', methods=['POST'])
def login_post():
    ...
    return redirect(url_for('main.profile'))