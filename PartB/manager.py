from flask import Blueprint, session, render_template, redirect
import os
import MySQLdb
import datetime
from calendar import monthrange
import pygal

managerbp = Blueprint("managerbp", __name__, template_folder="templates")
connection = MySQLdb.connect('34.126.127.197', "root", "duy298", "carshare_iot_system")
cursor = connection.cursor()


class Graph():
    @staticmethod
    def plot_booking_by_cars():
        curr_month = datetime.date.today().month
        x = []
        y = []

        cursor.execute("SELECT CarID, Name FROM Car")
        cars_list = cursor.fetchall()

        for row in cars_list:
            if row[0] not in x:
                x.append("{}:{}".format(row[0], row[1]))
                y.append(0)
        cursor.execute("SELECT CarID, bookTime FROM BookHistory")
        booking_list = cursor.fetchall()
        for row in booking_list:
            for i in range(0, len(x)):
                if x[i].split(":")[0] == str(row[0]) and row[1].month == curr_month:
                    y[i] = y[i] + 1
        # draw graph
        bar_chart = pygal.Bar()
        bar_chart.title = "Cars booked in current month"
        bar_chart.x_labels = x
        bar_chart.add("Booking", y)
        return bar_chart.render_data_uri()
    

    @staticmethod
    def plot_monthly_booking():
        x = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", 
        "November", "December"]
        y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        cursor.execute("SELECT CarID, bookTime FROM BookHistory")
        booking_list = cursor.fetchall()
        for row in booking_list:
            for i in range(len(x)):
                if row[1].month == i + 1:
                    y[i] = y[i] + 1
        # draw graph
        pie_chart = pygal.Pie()
        pie_chart.title = "Number of bookings monthly"
        for item in range(len(x)):
            pie_chart.add(x[item], y[item])

        return pie_chart.render_data_uri()


    @staticmethod
    def plot_daily_booking():
        today = datetime.date.today()
        day_of_month = monthrange(today.year, today.month)[1] 
        x=[]
        y=[]
        for j in range(day_of_month):
            cursor.execute("SELECT count(bookTime) FROM BookHistory WHERE month(bookTime)={} AND day(bookTime)={}".format(today.month, j+1))
            result = cursor.fetchall()
            x.append(j+1)
            y.append(result[0][0])

        # draw graph
        line_chart = pygal.Line()
        line_chart.title = "Daily booking amount in current month"
        line_chart.x_labels = x
        line_chart.add("Booking amount", y)

        return line_chart.render_data_uri()


@managerbp.route("/", methods=["GET"])
def managerHome():
    """
    Routing to manager's page
    """
    if ("user" in session) and (session["position"] == "manager"):
        managerHome = session["user"]

        bar_chart = Graph.plot_booking_by_cars()
        pie_chart = Graph.plot_monthly_booking()
        line_chart = Graph.plot_daily_booking()
        return render_template("manager.html", managerHome=managerHome, bar_chart=bar_chart, pie_chart=pie_chart, line_chart=line_chart)
    else:
        return redirect(url_for("login"))
        