from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import smtplib
import ssl

customerbp = Blueprint("customerbp", __name__, template_folder="templates")


@customerbp.route("/", methods=["GET"])
def customerHome():
    """
    Routing to customer's page
    """
    if ("user" in session) and (session["position"] == "customer"):
        return render_template("customers.html")
    else:
        return redirect(url_for("login"))
