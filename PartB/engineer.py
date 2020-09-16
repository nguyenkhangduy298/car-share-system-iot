from flask import Blueprint, render_template, redirect, session, url_for
from flask_googlemaps import Map
from geopy.geocoders import Nominatim

engineerbp = Blueprint("engineerbp",__name__, template_folder="templates")


@engineerbp.route("/", methods=["GET"])
def engineerHome():
    """
    Routing to engineer's page
    """
    if ("user" in session) and (session["position"] == "engineer"):
        return render_template("engineer.html")
    else:
        return redirect(url_for("login"))


@engineerbp.route("/viewmap", methods=["GET"])
def viewmap():
    """
    Routing to engineer's maintenace map page
    """
    if ("user" in session) and (session["position"] == "engineer"):
        from main import googlemaps, ReportedCar
        markers = ReportedCar.query.with_entities(ReportedCar.latitude, ReportedCar.longitude).all()
        if len(markers) > 0:
            maintenance_map = Map(
                identifier="view-side",
                lat=markers[0][0],
                lng=markers[0][1],
                markers=markers,
                fit_markers_to_bounds=True
            )
        else:
            maintenance_map = Map(
                identifier="view-map",
                # RMIT latitude and longitude
                lat=10.7294,
                lng=106.6931
            )
        return render_template("map.html", maintenance_map=maintenance_map)
    else:
        return redirect(url_for("login"))
