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
        adminHome = session["user"]
        return render_template("admin.html",adminHome= adminHome )
    else:
        return redirect(url_for("login"))


@adminbp.route("/report", methods=["GET", "POST"])
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


# Customer CRUD
@adminbp.route("/searchcustomer", methods=["GET", "POST"])
def searchCustomer():
    if ("user" in session) and (session["position"] == "admin"):
        from main import Customer
        if request.method == "POST":
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
                if len(customer_list) > 0:
                    result = ""
                    for customer in customer_list:
                        result = result + "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t <br>".format(customer.CustomerID,
                                                                                    customer.username,
                                                                                    customer.Name,
                                                                                    customer.address,
                                                                                    customer.phone,
                                                                                    customer.fax,
                                                                                    customer.email,
                                                                                    customer.contact)
                    return result
                else:
                    flash("Cannot find matching result")
                    return redirect(url_for("adminbp.searchCustomer"))
        else:
            return render_template("search_customer.html")
    else:
        return redirect(url_for("login"))


def searchCustomerById(customer_id):
    from main import Customer
    customer = Customer.query.filter_by(
        CustomerID=customer_id
    ).first()
    return customer


@adminbp.route("/removecustomer", methods=["GET", "POST"])
def removeCustomer():
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            from main import Customer, db
            customer_id = request.form["id"]
            customer = searchCustomerById(customer_id)
            if customer is not None:
                db.session.delete(customer)
                db.session.commit()
                flash("Removed successfully from the database")
                return redirect(url_for("adminbp.removeCustomer"))
            else:
                flash("Cannot find matching customer")
                return redirect(url_for("adminbp.removeCustomer"))
        else:
            return render_template("remove_customer.html")
        
    else:
        return redirect(url_for("login"))


@adminbp.route("/addcustomer", methods=["GET", "POST"])
def addCustomer():
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            from main import Customer, db
            username = request.form["username"]
            password = request.form["password"]
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            fax = request.form["fax"]
            email = request.form["email"]
            contact = request.form["contact"]
            customer = Customer(username, password, name, address, phone, fax, email, contact)
            db.session.add(customer)
            db.session.commit()
            flash("New customer added successfully")
            return redirect(url_for("adminbp.addCustomer"))
        else:
            return render_template("add_customer.html")
    else:
        return redirect(url_for("login"))


@adminbp.route("/modifycustomer", methods=["GET", "POST"])
def modifyCustomer():
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            try:
                from main import db
                customer_id = request.form["id"]
                customer = searchCustomerById(customer_id)
                # Update information
                customer.username = request.form["username"]
                customer.password = request.form["password"]
                customer.Name = request.form["name"]
                customer.address = request.form["address"]
                customer.phone = request.form["phone"]
                customer.fax = request.form["fax"]
                customer.email = request.form["email"]
                customer.contact = request.form["contact"]

                db.session.commit()
                flash("Information updated successfully")
                return redirect(url_for("adminbp.modifyCustomer"))
            except(AttributeError):
                flash("Cannot find the customer with given ID")
                return redirect(url_for("adminbp.modifyCustomer"))
        else:
            return render_template("modify_customer.html")
    else:
        return redirect(url_for("login"))


# Car CRUD
@adminbp.route("/searchcar", methods=["GET", "POST"])
def searchCar():
    if ("user" in session) and (session["position"] == "admin"):
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
                    return redirect(url_for("adminbp.searchCar"))
        else:
            return render_template("search_car.html")
    else:
        return redirect(url_for("login"))


def searchCarById(car_id):
    from main import Car
    car = Car.query.filter_by(
        CarID=car_id
    ).first()
    return car


@adminbp.route("/removecar", methods=["GET", "POST"])
def removeCar():
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            from main import Car, db
            car_id = request.form["id"]
            car = searchCarById(car_id)
            if car is not None:
                db.session.delete(car)
                db.session.commit()
                flash("Removed successfully from the database")
                return redirect(url_for("adminbp.removeCar"))
            else:
                flash("Cannot find matching car")
                return redirect(url_for("adminbp.removeCar"))
        else:
            return render_template("remove_car.html")
    else:
        return redirect(url_for("login"))


@adminbp.route("/addcar", methods=["GET", "POST"])
def addCar():
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            from main import Car, db
            status = request.form["status"]
            name = request.form["name"]
            model = request.form["model"]
            brand = request.form["brand"]
            company = request.form["company"]
            colour = request.form["colour"]
            seats = request.form["seats"]
            description = request.form["description"]
            category = request.form["category"]
            cost = request.form["cost"]
            location = request.form["location"]
            customer_id = request.form["customer"]
            car = Car(status, name, model, brand, company, colour, seats, description, category, cost, location, customer_id)
            db.session.add(car)
            db.session.commit()
            flash("New car added successfully")
            return redirect(url_for("adminbp.addCar"))
        else:
            return render_template("add_car.html")
    else:
        return redirect(url_for("login"))


@adminbp.route("/modifycar", methods=["GET", "POST"])
def modifyCar():
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            try:
                from main import db
                car_id = request.form["id"]
                car = searchCarById(car_id)
                # Update information
                car.status = request.form["status"]
                car.Name = request.form["name"]
                car.model = request.form["model"]
                car.brand = request.form["brand"]
                car.company = request.form["name"]
                car.colour = request.form["colour"]
                car.seats = request.form["seats"]
                car.description = request.form["description"]
                car.category = request.form["category"]
                car.cost_per_hour = request.form["cost"]
                car.location = request.form["location"]
                car.CustomerID = request.form["customer"]

                db.session.commit()
                flash("Information updated successfully")
                return redirect(url_for("adminbp.modifyCar"))
            except (AttributeError):
                flash("Cannot find the car with given ID")
                return redirect(url_for("adminbp.modifyCar"))
        else:
            return render_template("modify_car.html")
    else:
        return redirect(url_for("login"))
