from __future__ import print_function

from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from database_utils import DatabaseUtils

# from flask_login import login_required, current_user
# from email.mime.text import MIMEText
# from geopy.geocoders import Nominatim
# import smtplib
# import ssl
# import os

# [START calendar_quickstart]

from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

customerbp = Blueprint("customerbp", __name__, template_folder="templates")

# PEOPLE_FOLDER = os.path.join('static', 'people_photo')


@customerbp.route("/", methods=["GET"])
def customerHome():
    """
    Routing to admin's page
    """
    if ("user" in session) and (session["position"] == "customer"):
        customerHome = session["user"]
        return render_template("booking.html", customerHome=customerHome)
    else:
        return redirect(url_for("login"))

# @customerbp.route("/", methods=["GET"])
# def user():
#     """
#     Routing to customer's page
#     """
#     if ("user" in session) and (session["position"] == "customer"):
#         user = session["user"]
#         return render_template("customers.html", user = user)
#     else:
#         return redirect(url_for("login"))


@customerbp.route("/contact", methods=["GET"])
def customerContact():
    """
    Routing to customer's page
    """
    if ("user" in session) and (session["position"] == "customer"):
        return render_template("contactus.html")
    else:
        return redirect(url_for("login"))

# ...
# @customerbp.route('/login', methods=['POST'])
# def login_post():
#     ...
#     return redirect(url_for('main.profile'))

@customerbp.route("/history", methods=["GET"])
def viewCarList():
    """
        View User's Car List History
    """
    from main import Car
    from main import Login
    if ("user" in session) and (session["position"]=="customer"):
        car_list = Car.query.filter(Car.CustomerID==Login.ID).all()
        print(car_list)
        if len(car_list) > 0:
            result = ""
            for car in car_list:
                result = result + "{}\t{}\t{}\t{}\t{}\t{}\t{}\t <br>".format(car.Name,
                                                                            car.model,
                                                                            car.brand,
                                                                            car.colour,
                                                                            car.seats,
                                                                            car.company,
                                                                            car.description,
                                                                            car.category,
                                                                            car.cost_per_hour,
                                                                            car.location)
            return result
        else:
            flash("Cannot find matching result")
            return redirect(url_for("customerbp.searchCustomer"))
    else:
        return redirect(url_for("login"))

@customerbp.route("/searchcar", methods=["GET", "POST"])
def searchCar():
    """
        Search Car By Properties
    """
    if ("user" in session) and (session["position"] == "customer"):
        from main import Car
        if request.method == "POST":
            car_list = Car.query.filter(
                Car.CarID.like("%{}%".format(request.form["id"])),
                Car.status.like("%{}%".format(request.form["status"])),
                Car.Name.like("%{}%".format(request.form["name"])),
                Car.model.like("%{}%".format(request.form["model"])),
                Car.brand.like("%{}%".format(request.form["brand"])),
                Car.company.like("%{}%".format(request.form["company"])),
                Car.colour.like("%{}%".format(request.form["colour"])),
                Car.seats.like("%{}%".format(request.form["seats"])),
                Car.category.like("%{}%".format(request.form["category"])),
                Car.cost_per_hour.like("%{}%".format(request.form["cost"])),
                Car.location.like("%{}%".format(request.form["location"])),
                Car.CustomerID.like("%{}%".format(request.form["customer"]))
            ).all()
            if len(car_list) > 0:
                result = ""
                for car in car_list:
                    result = result + "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t <br>".format(car.CarID,
                                                                                                    car.status,
                                                                                                    car.Name,
                                                                                                    car.model,
                                                                                                    car.brand,
                                                                                                    car.company,
                                                                                                    car.colour,
                                                                                                    car.seats,
                                                                                                    car.description,
                                                                                                    car.category,
                                                                                                    car.cost_per_hour,
                                                                                                    car.location,
                                                                                                    car.CustomerID)
                return result
            else:
                flash("Cannot find any matching results")
                return redirect(url_for("customerbp.searchCar"))
        else:
            return render_template("search_car.html")
    else:
        return redirect(url_for("login"))


@customerbp.route("/bookCalendar", methods=["GET"])
def bookCalendar():
    """
        Booking Cars and Update in Google Calendar
    """

    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("token.json")
    creds = store.get()
    if (not creds or creds.invalid):
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build("calendar", "v3", http=creds.authorize(Http()))

    # Call the Calendar API.
    now = datetime.utcnow().isoformat() + "Z"  # "Z" indicates UTC time.
    print("Getting the upcoming 10 events.")
    events_result = service.events().list(calendarId="primary", timeMin=now,
                                          maxResults=10, singleEvents=True, orderBy="startTime").execute()
    events = events_result.get("items", [])

    if (not events):
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

    date = datetime(2020,9,30)
    start = date.strftime("%Y-%m-%d")
    time_start = "{}T06:00:00+10:00".format(start)
    date2 = datetime(2020,10,1)
    end = date2.strftime("%Y-%m-%d")
    time_end = "{}T07:00:00+10:00".format(end)
    event = {
        "summary": "Car Booking Duration",
        "location": "RMIT",
        "description": "Adding new IoT event",
        "start": {
            "dateTime": time_start,
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": time_end,
            "timeZone": "Asia/Tokyo",
        },
        "attendees": [
            {"email": "kduy298@gmail.com"},
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 5},
                {"method": "popup", "minutes": 10},
            ],
        }
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print("Event created: {}".format(event.get("htmlLink")))

    flash("Calendar Updated")
    flash("Car Booked")
    return redirect(url_for("customerbp.customerHome"))

def searchCarById(car_id):
    from main import Car
    car = Car.query.filter_by(
        CarID=car_id
    ).first()
    return car