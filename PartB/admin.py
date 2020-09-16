from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from passlib.hash import sha256_crypt

from admin import adminbp
from engineer import engineerbp

# Credentials for main database
HOST = "34.126.127.197"
USER = "root"
PASSWORD = "duy298"
DATABASE = "carshare_iot_system"

app = Flask(__name__)
app.register_blueprint(adminbp, url_prefix="/admin")
app.register_blueprint(engineerbp, url_prefix="/engineer")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretKey"

app.config["GOOGLEMAPS_KEY"] = "AIzaSyABKJGRjiU6RQMSDO46ZJeEoZkrtSWah_E"


db = SQLAlchemy(app)
googlemaps = GoogleMaps(app)


class Login(db.Model):
    """
    Represent the Executive table of remote database

    This is used to store the login credentials and position
    information of all registered executives. These data helps
    the process of logging in to the system as an executive.
    """
    __tablename__ = "Login"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    position = db.Column(db.String(100))

    def __init__(self, username, password, position):
        self.username = username
        self.password = password
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
                login = Login.query.filter_by(username=username).first()
                if (sha256_crypt.verify(password, login.password)):
                    session["user"] = login.username
                    session["position"] = login.position
                    if login.position == "admin":
                        return redirect(url_for("adminbp.adminHome"))
                    elif login.position == "manager":
                        return render_template("manager.html")
                    elif login.position == "engineer":
                        return redirect(url_for("engineerbp.engineerHome"))
                else:
                    flash("Wrong password!")
                    return render_template("login.html")
            except (AttributeError):
                flash("Cannot find user! Try again")
                return render_template("login.html")

        else:
            return render_template("login.html")
    else:
        if session["position"] == "admin":
            flash("You are already logged in as admin")
            return redirect(url_for("adminbp.adminHome"))
        elif session["position"] == "manager":
            flash("You are already logged in as manager")
            return render_template("manager.html")
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


@app.route("/registerexec", methods=["POST", "GET"])
def register():
    """
    Routing to page for registering executive account
    """
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        hashed_password = sha256_crypt.hash(password)
        position = request.form["position"]
        login = Login(username, hashed_password, position)
        db.session.add(login)
        db.session.commit()
        flash("Registered successfully")
        return redirect("login")
    else:
        return render_template("register.html")


@app.route("/manager", methods=["GET"])
def manager():
    """
    Routing to manager's page
    """
    if ("user" in session) and (session["position"] == "manager") :
        return render_template("manager.html")
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
