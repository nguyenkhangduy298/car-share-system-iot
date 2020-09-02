from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

HOST = "34.87.252.156"
USER = "root"
PASSWORD = "abc123"
DATABASE = "car_share_app"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretKey"

db = SQLAlchemy(app)


class Executive(db.Model):
    __tablename__ = "Executive"
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    position = db.Column(db.String(100))

    def __init__(self, username, password, position):
        self.username = username
        self.password = password
        self.position = position


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Routing to login page for executive
    """
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        try:
            executive = Executive.query.filter_by(username=username).first()
            if (sha256_crypt.verify(password, executive.password)):
                session["user"] = executive.username
                if executive.position == "admin":
                    return redirect(url_for("admin"))
                elif executive.position == "manager":
                    return "manager"
                elif executive.position == "engineer":
                    return "engineer"
            else:
                flash("Wrong password!")
                return render_template("login.html")
        except (AttributeError):
            flash("Cannot find user! Try again")
            return render_template("login.html")

    else:
        return render_template("login.html")


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
    if "user" in session:
        return render_template("manager.html")
    else:
        return redirect(url_for("login"))


@app.route("/admin", methods=["GET"])
def admin():
    """
    Routing to admin's page
    """
    if "user" in session:
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))


@app.route("/engineer", methods=["GET"])
def engineer():
    """
    Routing to engineer's page
    """
    if "user" in session:
        return render_template("engineer.html")
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
