import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load dataset (Replace with your actual dataset)
df = pd.read_csv("user_data.csv")

# Convert categorical data to numerical
df['transport_mode_encoded'] = df['transport_mode'].astype('category').cat.codes
df['electricity_source_encoded'] = df['electricity_source'].astype('category').cat.codes
df['heating_type_encoded'] = df['heating_type'].astype('category').cat.codes
df['energy_efficient_appliances_encoded'] = df['energy_efficient_appliances'].astype('category').cat.codes

# Define features (X) - Now includes ALL collected user inputs
X = df[[
    'beef_per_kg', 'chicken_per_kg', 'fish_per_kg', 'milk_liters_per_week', 'eggs_per_week',
    'vegan_meals_per_week', 'electricity_kwh_per_month', 'gas_usage_cubic_meters', 
    'electricity_source_encoded', 'heating_type_encoded', 'energy_efficient_appliances_encoded', 
    'distance_to_work', 'work_days', 'leisure_distance', 'transport_mode_encoded'
]]

# Define target variable (CO₂ reduction)
y = df['co2_reduction']

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "co2_reduction_model.pkl")

print("Updated model trained and saved as co2_reduction_model.pkl")
