import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from modules.db import (
    get_user_by_id,
    get_user_by_username,
    get_user_history,
    register_user,
    save_user_input,
)
from modules.diet_module import calculate_diet_footprint
from modules.energy_module import calculate_energy_footprint
from modules.form_parsers import parse_diet_form, parse_energy_form, parse_transport_form
from modules.recommendation_module import generate_logical_recommendations
from modules.transportation_module import calculate_transport_footprint

# Load local development environment variables from .env if present.
load_dotenv()


app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY") or secrets.token_urlsafe(32)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(user["id"], user["username"])
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if register_user(username, email, password):
            return redirect(url_for("login"))

        return "Username or email already exists. Try again."

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)
        if user and bcrypt.check_password_hash(user["password_hash"], password):
            login_user(User(user["id"], user["username"]))
            return redirect(url_for("index"))

        return "Invalid login credentials"

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/diet", methods=["GET", "POST"])
@login_required
def diet():
    if request.method == "POST":
        try:
            session["diet"] = parse_diet_form(request.form)
        except ValueError as exc:
            return render_template("diet.html", error=str(exc))
        return redirect(url_for("energy"))

    return render_template("diet.html")


@app.route("/energy", methods=["GET", "POST"])
@login_required
def energy():
    if request.method == "POST":
        try:
            session["energy"] = parse_energy_form(request.form)
        except ValueError as exc:
            return render_template("energy.html", error=str(exc))
        return redirect(url_for("transportation"))

    return render_template("energy.html")


@app.route("/transportation", methods=["GET", "POST"])
@login_required
def transportation():
    if request.method == "POST":
        try:
            session["transportation"] = parse_transport_form(request.form)
        except ValueError as exc:
            return render_template("transportation.html", error=str(exc)), 400
        return redirect(url_for("recommendations"))

    return render_template("transportation.html")


@app.route("/recommendations")
@login_required
def recommendations():
    if "diet" not in session:
        return redirect(url_for("diet"))
    if "energy" not in session:
        return redirect(url_for("energy"))
    if "transportation" not in session:
        return redirect(url_for("transportation"))

    diet_footprint = calculate_diet_footprint(session["diet"])
    energy_footprint = calculate_energy_footprint(session["energy"])
    transport_footprint = calculate_transport_footprint(session["transportation"])

    user_footprints = {
        "diet": diet_footprint,
        "energy": energy_footprint,
        "transportation": transport_footprint,
    }

    save_user_input(
        user_id=current_user.id,
        diet_data=session["diet"],
        energy_data=session["energy"],
        transport_data=session["transportation"],
        diet_footprint=diet_footprint,
        energy_footprint=energy_footprint,
        transport_footprint=transport_footprint,
    )

    recommendations_data = generate_logical_recommendations(
        session["transportation"],
        session["diet"],
        session["energy"],
        user_footprints,
    )

    return render_template("recommendation.html", recommendations=recommendations_data)


@app.route("/history")
@login_required
def history():
    history_data = get_user_history(current_user.id)

    if not history_data:
        return render_template("history.html", history=[], best_record=None)

    min_total = min(
        entry["diet_footprint"] + entry["energy_footprint"] + entry["transport_footprint"]
        for entry in history_data
    )

    for i, entry in enumerate(history_data):
        total = (
            entry["diet_footprint"]
            + entry["energy_footprint"]
            + entry["transport_footprint"]
        )
        entry["total_footprint"] = total

        if i == len(history_data) - 1:
            entry["change"] = 0
            entry["is_best"] = False
        else:
            prev = history_data[i + 1]
            prev_total = (
                prev["diet_footprint"]
                + prev["energy_footprint"]
                + prev["transport_footprint"]
            )
            entry["change"] = total - prev_total

        entry["is_best"] = total == min_total

    return render_template("history.html", history=history_data)


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
