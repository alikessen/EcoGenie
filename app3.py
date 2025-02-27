import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import joblib
from modules.diet_module import calculateDietFootprint
from modules.energy_module import calculateEnergyFootprint
from modules.transportation import calculateTransportFootprint
from modules.recommendation_module import generateLogicalRecommendations

app = Flask(__name__, static_folder="static")

# Load trained model
model = joblib.load("co2_reduction_model.pkl")

user_data = {}

# Define CSV file for storing user responses
CSV_FILE = "user_data.csv"

def save_user_data():
    """Save user responses to CSV for future model training."""
    new_data = {
        "beef_per_kg": user_data['diet']['beef_per_kg'],
        "chicken_per_kg": user_data['diet']['chicken_per_kg'],
        "fish_per_kg": user_data['diet']['fish_per_kg'],
        "milk_liters_per_week": user_data['diet']['milk_liters_per_week'],
        "eggs_per_week": user_data['diet']['eggs_per_week'],
        "vegan_meals_per_week": user_data['diet']['vegan_meals_per_week'],
        "electricity_kwh_per_month": user_data['energy']['electricity_kwh_per_month'],
        "gas_usage_cubic_meters": user_data['energy']['gas_usage_cubic_meters'],
        "electricity_source": user_data['energy']['electricity_source'],
        "heating_type": user_data['energy']['heating_type'],
        "energy_efficient_appliances": user_data['energy']['energy_efficient_appliances'],
        "distance_to_work": user_data['transportation']['distance_to_work'],
        "work_days": user_data['transportation']['work_days'],
        "leisure_distance": user_data['transportation']['leisure_distance'],
        "transport_mode": user_data['transportation']['mode_of_transport']
    }

    # Convert to DataFrame
    df = pd.DataFrame([new_data])

    # If file exists, append without header; otherwise, create it
    file_exists = os.path.isfile(CSV_FILE)
    df.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)
    print("✅ User data saved to", CSV_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diet', methods=['GET', 'POST'])
def diet():
    if request.method == 'POST':
        user_data['diet'] = {
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
def energy():
    if request.method == 'POST':
        user_data['energy'] = {
            "electricity_kwh_per_month": float(request.form.get('electricity_kwh_per_month', '0') or 0),
            "electricity_source": request.form['electricity_source'],
            "heating_type": request.form['heating_type'],
            "gas_usage_cubic_meters": float(request.form.get('gas_usage_cubic_meters', '0') or 0),
            "energy_efficient_appliances": request.form['energy_efficient_appliances']
        }
        return redirect(url_for('transportation'))
    return render_template('energy.html')

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    if request.method == 'POST':
        user_data['transportation'] = {
            "mode_of_transport": request.form.get('mode_of_transport', ''),
            "distance_to_work": float(request.form.get('distance_to_work', '0') or 0),
            "work_days": int(request.form.get('work_days', '0') or 0),
            "leisure_distance": float(request.form.get('leisure_distance', '0') or 0)
        }
        return redirect(url_for('recommendations'))
    return render_template('transportation.html')

@app.route('/recommendations')
def recommendations():
    if not user_data:
        return redirect(url_for('index'))

    # Calculate carbon footprint
    diet_footprint = calculateDietFootprint(user_data['diet'])
    energy_footprint = calculateEnergyFootprint(user_data['energy'])
    transport_footprint = calculateTransportFootprint(user_data['transportation'])

    # Save user data to CSV for model training
    save_user_data()

    # Generate recommendations
    logical_recommendations = generateLogicalRecommendations(
        user_data['transportation'], user_data['diet'], user_data['energy'],
        {"diet": diet_footprint, "energy": energy_footprint, "transportation": transport_footprint}
    )

    return render_template('recommendation.html', recommendations=logical_recommendations)

if __name__ == '__main__':
    app.run(debug=True)
