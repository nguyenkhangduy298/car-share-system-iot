from flask import Blueprint, render_template, session, redirect, url_for, request
from email.mime.text import MIMEText
import smtplib
import ssl

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/", methods=["GET"])
def adminHome():
    """
    Routing to admin's page
    """
    if ("user" in session) and (session["position"] == "admin"):
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))


@admin.route("/send", methods = ["GET", "POST"])
def sendEmail():
    """
    Send email to engineer when admin report a car
    """
    if ("user" in session) and (session["position"] == "admin"):
        if request.method == "POST":
            port = 587
            smtp_server = "smtp.office365.com"
            sender = "s3694615@rmit.edu.vn"
            receivers = ["s3694615@rmit.edu.vn", "dkhoilaska@gmail.com"]
            password = request.form["password"]

            message = request.form["content"]
            mail = MIMEText(message)
            mail["Subject"] = "Testing message"
            mail["To"] = ", ".join(receivers)
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.login(sender, password)
                    server.sendmail(sender, receivers, mail.as_string())
            except (smtplib.SMTPAuthenticationError):
                return "Wrong username or password"
            return "Emails are sent"
        else:
            return render_template("email.html")
    else:
        return redirect(url_for("login"))
