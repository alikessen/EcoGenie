# Import Flask modules and necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Import project modules
from modules.diet_module import calculateDietFootprint
from modules.energy_module import calculateEnergyFootprint
from modules.transportation_module import calculateTransportFootprint
from modules.recommendation_module import generateLogicalRecommendations
from modules.db import register_user, get_user_by_username, get_user_by_id, save_user_input, get_user_history


# Create Flask application instance
app = Flask(__name__, static_folder="static")  
app.secret_key = "secret_key" # Used for session management

# Setup bcrypt for password hashing
bcrypt = Bcrypt(app)

# Setup Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirects users to login page if not logged in

# Define user class for Flask-Login
class User(UserMixin):
    """User class for Flask-Login."""
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Load user session from user ID
@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)  
    if user:
        return User(user["id"], user["username"])
    return None

# Home page route
@app.route('/')
def index():
    if current_user.is_authenticated:
        print("Logged in as:", current_user.username)
    else:
        print("Not logged in.")
    return render_template('index.html')

# Registration route
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
    return redirect(url_for("index"))

# Diet form route
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


# Energy form route
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


# Transportation form route
@app.route('/transportation', methods=['GET', 'POST'])
@login_required
def transportation():
    if request.method == 'POST':
        try:
            working = request.form.get("working", "")
            work_distance_km = 0
            work_days = 0
            work_mode = ""
            work_car_type = ""
            work_pt_type = ""
            
            # Handle work travel inputs
            if working == "yes":

                work_mode = request.form.get("work_mode", "")
                if work_mode == "car":
                    work_car_type = request.form.get("work_car_type", "")
                elif work_mode == "public transport":
                    work_pt_type = request.form.get("work_pt_type", "")
                work_distance_km = float(request.form.get("work_distance_km", 0))
                work_days = int(request.form.get("work_days", 0))

            # Handle leisure travel inputs
            try:
                leisure_distance = float(request.form.get("leisure_distance") or 0)
            except ValueError:
                leisure_distance = 0

            try:
                leisure_days = int(request.form.get("leisure_days") or 0)
            except ValueError:
                leisure_days = 0

            session["transportation"] = {
                "working": working,
                "work_distance_km": work_distance_km,
                "work_days": work_days,
                "work_mode": work_mode,
                "work_car_type": work_car_type,
                "work_pt_type": work_pt_type,
                "leisure_distance": leisure_distance,
                "leisure_days": leisure_days,
                "leisure_mode": request.form.get("leisure_mode", ""),
                "leisure_type": request.form.get("leisure_type", "")
            }

        except ValueError as e:
            print("Error converting input:", e)
            return render_template('transportation.html', error="Invalid input. Please enter numbers only.")
        
        return redirect(url_for('recommendations'))

    return render_template('transportation.html')


# Recommendation display route
@app.route('/recommendations')
@login_required
def recommendations():
    if 'diet' not in session:
        return redirect(url_for('diet'))

    if 'energy' not in session:
        return redirect(url_for('energy'))

    if 'transportation' not in session:
        return redirect(url_for('transportation'))

    # Calculate footprints
    diet_footprint = calculateDietFootprint(session['diet'])
    energy_footprint = calculateEnergyFootprint(session['energy'])
    transport_footprint = calculateTransportFootprint(session['transportation'])

    user_footprints = {
        "diet": diet_footprint,
        "energy": energy_footprint,
        "transportation": transport_footprint
    }

     # Save data to database
    save_user_input(
        user_id=current_user.id,
        diet_data=session['diet'],
        energy_data=session['energy'],
        transport_data=session['transportation'],
        diet_footprint=diet_footprint,
        energy_footprint=energy_footprint,
        transport_footprint=transport_footprint
    )

    # Generate recommendations
    recommendations = generateLogicalRecommendations(
        session['transportation'], session['diet'], session['energy'], user_footprints
    )

    return render_template('recommendation.html', recommendations=recommendations)


# History display route
@app.route('/history')
@login_required
def history():
    history_data = get_user_history(current_user.id)

    if not history_data:
        return render_template("history.html", history=[], best_record=None)
    
    # Identify best record and calculate change
    min_total = min(e['diet_footprint'] + e['energy_footprint'] + e['transport_footprint'] for e in history_data)

    for i, entry in enumerate(history_data):
        total = entry['diet_footprint'] + entry['energy_footprint'] + entry['transport_footprint']
        entry['total_footprint'] = total
        if i == len(history_data) - 1:
            entry['change'] = 0
            entry['is_best'] = False
        else:
           prev_total = history_data[i + 1]['diet_footprint'] + history_data[i + 1]['energy_footprint'] + history_data[i + 1]['transport_footprint']
           entry['change'] = total - prev_total

        entry['is_best'] = total == min_total
        
    return render_template("history.html", history=history_data)



# Start the app
if __name__ == '__main__':
    app.run(debug=True)
