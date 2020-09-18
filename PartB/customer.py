from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import smtplib
import ssl
import os

customerbp = Blueprint("customerbp", __name__, template_folder="templates")
#PEOPLE_FOLDER = os.path.join('static', 'people_photo')
@customerbp.route("/", methods=["GET"])
def customerHome():
    """
    Routing to customer's page
    """
    if ("user" in session) and (session["position"] == "customer"):
        #full_filename = os.path.join('images/product-6-720x480.jpg')
        return render_template("booking.html")
    else:
        return redirect(url_for("login"))
