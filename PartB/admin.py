from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import smtplib
import ssl

adminbp = Blueprint("adminbp", __name__, template_folder="templates")


@adminbp.route("/", methods=["GET"])
def adminHome():
    """
    Routing to admin's page
    """
    if ("user" in session) and (session["position"] == "admin"):
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))


@adminbp.route("/send", methods=["GET","POST"])
def sendEmail():
    """
    Send email to engineers when admin report a car
    """
    if ("user" in session) and (session["position"] == "admin"):
        from main import ReportedCar, db

        if request.method == "POST":
            # Email configuration
            port = 587
            smtp_server = "smtp.office365.com"
            receivers = ["s3694615@rmit.edu.vn", "dkhoilaska@gmail.com"]
            sender = request.form["email"]
            password = request.form["password"]
            location = request.form["location"]

            # Use geopy library to get location latitude, longitude
            try:
                geolocator = Nominatim(user_agent="app")
                place = geolocator.geocode(location)
                car_location = ReportedCar(location, place.latitude, place.longitude)
                db.session.add(car_location)
            except (AttributeError):
                flash("Cannot find the specified location")
                return redirect(url_for("adminbp.sendEmail"))

            # Compose email
            message = "Car needs maintenance at: " + location + "\n(" + place.address + ")"
            mail = MIMEText(message)
            mail["Subject"] = "Testing message"
            mail["To"] = ", ".join(receivers)

            # Send email
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.login(sender, password)

                    db.session.commit()  # Only store to database when login successfully
                    server.sendmail(sender, receivers, mail.as_string())
            except (smtplib.SMTPAuthenticationError):
                flash("Wrong username or password")
                return redirect(url_for("adminbp.sendEmail"))
            flash("Emails are sent to engineers")
            return redirect(url_for("adminbp.sendEmail"))
        else:
            return render_template("report.html")
    else:
        return redirect(url_for("login"))

@adminbp.route("/searchcustomer", methods=["GET", "POST"])
def searchCustomer():
    if ("user" in session) and (session["position"] == "admin"):
        from main import Customer
        if request.method == "POST":
            try:
                customer_list = Customer.query.filter(
                    Customer.CustomerID.like("%{}%".format(request.form["id"])),
                    Customer.username.like("%{}%".format(request.form["username"])),
                    Customer.Name.like("%{}%".format(request.form["name"])),
                    Customer.address.like("%{}%".format(request.form["address"])),
                    Customer.phone.like("%{}%".format(request.form["phone"])),
                    Customer.fax.like("%{}%".format(request.form["fax"])),
                    Customer.email.like("%{}%".format(request.form["email"])),
                    Customer.contact.like("%{}%".format(request.form["contact"]))
                ).all()
                result = ""
                for customer in customer_list:
                    print(customer.Name)
                    result = result + "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t\n".format(customer.CustomerID,
                                                                                    customer.username,
                                                                                    customer.Name,
                                                                                    customer.address,
                                                                                    customer.phone,
                                                                                    customer.fax,
                                                                                    customer.email,
                                                                                    customer.contact)
                return result
            except (IndexError):
                flash("Cannot find any matching results")
                return redirect(url_for("adminbp.searchCustomer"))

        else:
            return render_template("search_customer.html")
    else:
        return redirect(url_for("login"))
