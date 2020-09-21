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
#PEOPLE_FOLDER = os.path.join('static', 'people_photo')
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

...
@customerbp.route('/login', methods=['POST'])
def login_post():
    ...
    return redirect(url_for('main.profile'))

@customerbp.route("/history", methods=["GET"])
def viewCarList():
    """
        View User's Car List History
    """
    from main import Car
    car_list = Car.query.filter(Car.CustomerID==8).all()
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

    date = datetime.now()
    tomorrow = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    time_start = "{}T06:00:00+10:00".format(tomorrow)
    time_end = "{}T07:00:00+10:00".format(tomorrow)
    event = {
        "summary": "New Programmatic Event",
        "location": "RMIT Building 14",
        "description": "Adding new IoT event",
        "start": {
            "dateTime": time_start,
            "timeZone": "Australia/Melbourne",
        },
        "end": {
            "dateTime": time_end,
            "timeZone": "Australia/Melbourne",
        },
        "attendees": [
            {"email": "kevin@scare.you"},
            {"email": "shekhar@wake.you"},
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

# [END calendar_quickstart]