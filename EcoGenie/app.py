from flask import Flask, render_template, request, redirect, url_for
from modules.diet_module import getDietData, calculateDietFootprint
from modules.energy_module import getEnergyData, calculateEnergyFootprint
from modules.transportation import getTransportationData, calculateTransportFootprint
from modules.recommendation_module import generateLogicalRecommendations

app = Flask(__name__)

user_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diet', methods=['GET', 'POST'])
def diet():
    if request.method == 'POST':
        user_data['diet'] = {
            "diet_type": request.form['diet_type'],
            "beef_per_kg": float(request.form.get('beef_per_kg', 0)),
            "chicken_per_kg": float(request.form.get('chicken_per_kg', 0)),
            "fish_per_kg": float(request.form.get('fish_per_kg', 0)),
            "milk_liters_per_week": float(request.form.get('milk_liters_per_week', 0)),
            "eggs_per_week": int(request.form.get('eggs_per_week', 0)),
            "vegan_meals_per_week": int(request.form.get('vegan_meals_per_week', 0))
        }
        return redirect(url_for('energy'))
    return render_template('diet.html')

@app.route('/energy', methods=['GET', 'POST'])
def energy():
    if request.method == 'POST':
        user_data['energy'] = {
            "electricity_kwh_per_month": float(request.form['electricity_kwh_per_month']),
            "electricity_source": request.form['electricity_source'],
            "heating_type": request.form['heating_type'],
            "gas_usage_cubic_meters": float(request.form.get('gas_usage_cubic_meters', 0)),
            "energy_efficient_appliances": request.form['energy_efficient_appliances']
        }
        return redirect(url_for('transportation'))
    return render_template('energy.html')

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    if request.method == 'POST':
        distance_to_work = float(request.form.get('distance_to_work', 0))
        mode_of_transport = request.form['mode_of_transport']
        work_type = request.form.get('work_type', '')  # 🔥 Fix: Use 'work_type' instead of 'type'

        # Compute total distance (assuming a 5-day work week)
        total_distance = distance_to_work * 2 * 5  # Round-trip, 5 times a week

        user_data['transportation'] = {
            "work_mode": mode_of_transport,
            "distance_to_work": distance_to_work,
            "total_distance": total_distance,
            "work_type": work_type  # 🔥 Fix applied
        }
        return redirect(url_for('recommendations'))

    return render_template('transportation.html')


@app.route('/recommendations')
def recommendations():
    if not user_data:
        return redirect(url_for('index'))
    
    diet_footprint = calculateDietFootprint(user_data['diet'])
    energy_footprint = calculateEnergyFootprint(user_data['energy'])
    transport_footprint = calculateTransportFootprint(user_data['transportation'])
    
    user_footprints = {
        "diet": diet_footprint,
        "energy": energy_footprint,
        "transportation": transport_footprint
    }
    
    recommendations = generateLogicalRecommendations(user_data['transportation'], user_data['diet'], user_data['energy'], user_footprints)
    
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
