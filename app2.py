from flask import Flask, render_template, request, redirect, url_for
from modules.diet_module import getDietData, calculateDietFootprint
from modules.energy_module import getEnergyData, calculateEnergyFootprint
from modules.transportation import getTransportData, calculateTransportFootprint
from modules.recommendation_module import generateLogicalRecommendations

app = Flask(__name__, static_folder="static")  # Ensure static folder is accessible

user_data = {}  # Temporary storage for user inputs

# Home Page 
@app.route('/')
def index():
    return render_template('index.html')

# Diet Input Page 
@app.route('/diet', methods=['GET', 'POST'])
def diet():
    if request.method == 'POST':
        print("Form Data Received:", request.form)  # Debugging output

        try:
            user_data['diet'] = {
                "diet_type": request.form['diet_type'],
                "beef_per_kg": float(request.form.get('beef_per_kg', '0') or 0),
                "chicken_per_kg": float(request.form.get('chicken_per_kg', '0') or 0),
                "fish_per_kg": float(request.form.get('fish_per_kg', '0') or 0),
                "milk_liters_per_week": float(request.form.get('milk_liters_per_week', '0') or 0),
                "eggs_per_week": int(request.form.get('eggs_per_week', '0') or 0),
                "vegan_meals_per_week": int(request.form.get('vegan_meals_per_week', '0') or 0)
            }
        except ValueError as e:
            print("Error converting input:", e)  # Debugging error
            return render_template('diet.html', error="Invalid input. Please enter numbers only.")

        return redirect(url_for('energy'))

    return render_template('diet.html')


# Energy Input Page 
@app.route('/energy', methods=['GET', 'POST'])
def energy():
    if request.method == 'POST':
        try:
            user_data['energy'] = {
                "electricity_kwh_per_month": float(request.form.get('electricity_kwh_per_month', '0') or 0),
                "electricity_source": request.form['electricity_source'],
                "heating_type": request.form['heating_type'],
                "gas_usage_cubic_meters": float(request.form.get('gas_usage_cubic_meters', '0') or 0),  
                "energy_efficient_appliances": request.form['energy_efficient_appliances']
            }
        except ValueError as e:
            print("Error converting input:", e)  # Debugging output
            return render_template('energy.html', error="Invalid input. Please enter valid numbers.")

        return redirect(url_for('transportation'))
    
    return render_template('energy.html')

# Transportation Input Page 
@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    if request.method == 'POST':
        print("Form Data Received:", request.form)  # Debugging output

        try:
            user_data['transportation'] = {
                "work_distance_km": float(request.form.get("work_distance_km", 0)),  # Fix: Use .get()
                "work_days": int(request.form.get("work_days", 0)),
                "work_mode": request.form.get("work_mode", ""),
                "work_type": request.form.get("work_type", ""),
            }
        except ValueError as e:
            print("Error converting input:", e)  # Debugging output
            return render_template('transportation.html', error="Invalid input. Please enter numbers only.")

        print("Transportation Data Stored:", user_data['transportation'])  # Debugging output

        return redirect(url_for('recommendations'))

    return render_template('transportation.html')


# Generate Recommendations 
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
    
    return render_template('recommendation.html', recommendations=recommendations)

# Run Flask App 
if __name__ == '__main__':
    app.run(debug=True)
