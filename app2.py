from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from modules.diet_module import getDietData, calculateDietFootprint
from modules.energy_module import getEnergyData, calculateEnergyFootprint
from modules.transportation import getTransportData, calculateTransportFootprint
from modules.recommendation_module import generateLogicalRecommendations
from modules.db import get_db_connection, register_user, get_user_by_username, get_user_by_id


# Flask App
app = Flask(__name__, static_folder="static")  # Keep only one Flask instance
app.secret_key = "secret_key"

# Flask-Login & Bcrypt Setup
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirects users to login page if not logged in

# User Class
class User(UserMixin):
    """User class for Flask-Login."""
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)  # <- FIXED: now using correct ID lookup
    if user:
        return User(user["id"], user["username"])
    return None

# Home Page
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if register_user(username, email, password):
            return redirect(url_for('login'))
        else:
            return "Username or email already exists. Try again."

    return render_template("register.html")

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)
        if user and bcrypt.check_password_hash(user["password_hash"], password):
            login_user(User(user["id"], user["username"]))
            return redirect(url_for("index"))
        else:
            return "Invalid login credentials"

    return render_template("login.html")

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Diet Page
@app.route('/diet', methods=['GET', 'POST'])
@login_required
def diet():
    if request.method == 'POST':
        session["diet"] = {  
            "diet_type": request.form.get('diet_type', ''),
            "beef_per_kg": float(request.form.get('beef_per_kg', '0') or 0),
            "chicken_per_kg": float(request.form.get('chicken_per_kg', '0') or 0),
            "fish_per_kg": float(request.form.get('fish_per_kg', '0') or 0),
            "milk_liters_per_week": float(request.form.get('milk_liters_per_week', '0') or 0),
            "eggs_per_week": int(request.form.get('eggs_per_week', '0') or 0),
            "vegan_meals_per_week": int(request.form.get('vegan_meals_per_week', '0') or 0)
        }
        return redirect(url_for('energy'))

    return render_template('diet.html')

@app.route('/energy', methods=['GET', 'POST'])
@login_required
def energy():
    if request.method == 'POST':
        try:
            session["energy"] = {
                "electricity_kwh_per_month": float(request.form.get('electricity_kwh_per_month', '0') or 0),
                "electricity_source": request.form.get('electricity_source', ''),
                "heating_type": request.form.get('heating_type', ''),
                "gas_usage_cubic_meters": float(request.form.get('gas_usage_cubic_meters', '0') or 0),
                "energy_efficient_appliances": request.form.get('energy_efficient_appliances', '')
            }
        except ValueError as e:
            print("Error converting input:", e)
            return render_template('energy.html', error="Invalid input. Please enter valid numbers.")
        
        return redirect(url_for('transportation'))

    return render_template('energy.html')

@app.route('/transportation', methods=['GET', 'POST'])
@login_required
def transportation():
    if request.method == 'POST':
        try:
            session["transportation"] = {
                "work_distance_km": float(request.form.get("work_distance_km", 0)),
                "work_days": int(request.form.get("work_days", 0)),
                "work_mode": request.form.get("work_mode", ""),
                "work_type": request.form.get("work_type", "")
            }
        except ValueError as e:
            print("Error converting input:", e)
            return render_template('transportation.html', error="Invalid input. Please enter numbers only.")
        
        return redirect(url_for('recommendations'))

    return render_template('transportation.html')


# Recommendations
@app.route('/recommendations')
@login_required
def recommendations():
    if 'diet' not in session:
        return redirect(url_for('diet'))

    if 'energy' not in session:
        return redirect(url_for('energy'))

    if 'transportation' not in session:
        return redirect(url_for('transportation'))

    diet_footprint = calculateDietFootprint(session['diet'])
    energy_footprint = calculateEnergyFootprint(session['energy'])
    transport_footprint = calculateTransportFootprint(session['transportation'])

    user_footprints = {
        "diet": diet_footprint,
        "energy": energy_footprint,
        "transportation": transport_footprint
    }

    recommendations = generateLogicalRecommendations(
        session['transportation'], session['diet'], session['energy'], user_footprints
    )

    return render_template('recommendation.html', recommendations=recommendations)

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
