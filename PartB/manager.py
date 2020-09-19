from flask import Blueprint, session, render_template, redirect

managerbp = Blueprint("managerbp", __name__, template_folder="templates")

@managerbp.route("/", methods=["GET"])
def managerHome():
    """
    Routing to manager's page
    """
    if ("user" in session) and (session["position"] == "manager") :
        return render_template("manager.html")
    else:
        return redirect(url_for("login"))
