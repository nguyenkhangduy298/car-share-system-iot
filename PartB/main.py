from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from passlib.hash import sha256_crypt

from admin import adminbp
from engineer import engineerbp

HOST = "34.87.252.156"
USER = "root"
PASSWORD = "abc123"
DATABASE = "car_share_app"

app = Flask(__name__)
app.register_blueprint(adminbp, url_prefix="/admin")
app.register_blueprint(engineerbp, url_prefix="/engineer")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretKey"

db = SQLAlchemy(app)
googlemaps = GoogleMaps(app)


class Executive(db.Model):
    __tablename__ = "Executive"
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    position = db.Column(db.String(100))

    def __init__(self, username, password, position):
        self.username = username
        self.password = password
        self.position = position


class ReportedCar(db.Model):
    __tablename__ = "ReportedCar"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, location, latitude, longitude):
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

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
                executive = Executive.query.filter_by(username=username).first()
                if (sha256_crypt.verify(password, executive.password)):
                    session["user"] = executive.username
                    session["position"] = executive.position
                    if executive.position == "admin":
                        return redirect(url_for("adminbp.adminHome"))
                    elif executive.position == "manager":
                        return "manager"
                    elif executive.position == "engineer":
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
            return "manager"
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
        executive = Executive(username, hashed_password, position)
        db.session.add(executive)
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
    if ("user" in session) and (session["position"] == "manager"):
        return render_template("manager.html")
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
