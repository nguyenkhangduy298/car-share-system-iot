from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from passlib.hash import sha256_crypt

from admin import adminbp
from engineer import engineerbp
from customer import customerbp
from manager import managerbp

# Credentials for main database
HOST = "34.126.127.197"
USER = "root"
PASSWORD = "duy298"
DATABASE = "carshare_iot_system"

app = Flask(__name__)
app.register_blueprint(adminbp, url_prefix="/admin")
app.register_blueprint(customerbp, url_prefix="/customer")
app.register_blueprint(engineerbp, url_prefix="/engineer")
app.register_blueprint(managerbp, url_prefix="/manager")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretKey"

app.config["GOOGLEMAPS_KEY"] = "AIzaSyAguVQ25U6PQbgESlC4jxCxk-3BcYGksW4"


db = SQLAlchemy(app)
googlemaps = GoogleMaps(app)


class Person(db.Model):
    """
        Represent the Person table of remote database

        This is used to store the login credentials and position
        information of all person. These data helps
        the process of logging in to the system.
    """
    __tablename__ = "Person"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    position = db.Column(db.Integer)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    phone = db.Column(db.Text)
    fax = db.Column(db.Text)
    email = db.Column(db.Text)
    contact = db.Column(db.Text)
    image = db.Column(db.Text)

    def __init__(self, username, password, position, name, address, phone, fax, email, contact, image):
        self.username = username
        self.password = password
        self.position = position
        self.name = name
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.contact = contact
        self.image = image



class Role(db.Model):
    __tablename__ = "Role"
    ID = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Text)

    def __init__(self, position):
        self.position = position


class ReportedCar(db.Model):
    """
    Represent the ReportedCar table of the remote database
    """
    __tablename__ = "ReportedCar"
    ID = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, location, latitude, longitude):
        self.location = location
        self.latitude = latitude
        self.longitude = longitude


class Customer(db.Model):
    __tablename__ = "Customer"
    CustomerID = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    Name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.Text)
    fax = db.Column(db.Text)
    email = db.Column(db.Text)
    contact = db.Column(db.Text)

    def __init__(self, username, password, Name, address, phone, fax, email, contact):
        self.username = username
        self.password = password
        self.Name = Name
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.contact = contact


class Car(db.Model):
    __tablename__ = "Car"
    CarID = db.Column(db.Integer, nullable=False, primary_key=True)
    status = db.Column(db.Text)
    Name = db.Column(db.Text, nullable=False)
    model = db.Column(db.Text)
    brand = db.Column(db.Text)
    company = db.Column(db.Text)
    colour = db.Column(db.Text)
    seats = db.Column(db.Integer)
    description = db.Column(db.Text)
    category = db.Column(db.Text)
    cost_per_hour = db.Column(db.Float(precision=53), nullable=False)
    location = db.Column(db.Text)
    CustomerID = db.Column(db.Integer)

    def __init__(self, status, Name, model, brand, company, colour, seats, description, category, cost_per_hour, location, CustomerID):
        self.status = status
        self.Name = Name
        self.model = model
        self.brand = brand
        self.company = company
        self.colour = colour
        self.seats = seats
        self.description = description
        self.category = category
        self.cost_per_hour = cost_per_hour
        self.location = location
        self.CustomerID = CustomerID


class BookHistory(db.Model):
    __tablename__ = "BookHistory"
    HistoryID = db.Column(db.Integer, nullable=False, primary_key=True)
    status = db.Column(db.Text)
    carID = db.Column(db.Integer, nullable=False)
    customerID = db.Column(db.Integer, nullable=False)
    bookTime = db.Column(db.Date, nullable=False)
    endTime = db.Column(db.Date, nullable=False)

    def __init__(self, HistoryID, status, carID, customerID, bookTime, endTime):
        self.HistoryID = HistoryID
        self.status = status
        self.carID = carID
        self.customerID = customerID
        self.bookTime = bookTime
        self.endTime = endTime


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Routing to login page for executive
    """
    if "user" not in session:
        if request.method == "POST":
            username = request.form["name"]
            password = request.form["password"]
            try:
                person = Person.query.filter_by(username=username).first()
                print(person.position)
            except (AttributeError):
                flash("Cannot find user! Try again")
                return redirect(url_for("login"))
            if (sha256_crypt.verify(password, person.password)):
                session["user"] = person.username
                role = Role.query.filter_by(ID=person.position).first()
                session["position"] = role.position
                if role.position == "admin":
                    return redirect(url_for("adminbp.adminHome"))
                elif role.position == "customer":
                    return redirect(url_for("customerbp.customerHome"))
                elif role.position == "manager":
                    return redirect(url_for("managerbp.managerHome"))
                elif role.position == "engineer":
                    return redirect(url_for("engineerbp.engineerHome"))
            else:
                flash("Wrong password!")
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        if session["position"] == "admin":
            flash("You are already logged in as admin")
            return redirect(url_for("adminbp.adminHome"))
        elif session["position"] == "customer":
            flash("You are already logged in as customer")
            return redirect(url_for("customerbp.customerHome"))
        elif session["position"] == "manager":
            flash("You are already logged in as manager")
            return redirect(url_for("managerbp.managerHome"))
        elif session["position"] == "engineer":
            flash("You are already logged in as engineer")
            return redirect(url_for("engineerbp.engineerHome"))


@app.route("/logout")
def logout():
    """
    Log out from current session user
    """
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Routing to page for registering executive account
    """
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        hashed_password = sha256_crypt.hash(password)
        position = request.form["position"]
        role = Role.query.filter_by(position=position).first()
        positionID = role.ID
        person = Person(username, hashed_password, positionID, "", "", "", "", "", "", "",)
        db.session.add(person)
        db.session.commit()
        flash("Registered successfully")
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


if __name__ == '__main__':
    db.create_all()
    if Role.query.all() == []:
        admin = Role("admin")
        manager = Role("manager")
        engineer = Role("engineer")
        customer = Role("customer")
        db.session.add(admin)
        db.session.add(manager)
        db.session.add(engineer)
        db.session.add(customer)
        db.session.commit()
    app.run(debug=True)
