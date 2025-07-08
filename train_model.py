# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load the dataset
df = pd.read_excel("Harvest.xlsx", sheet_name="Harvest Report")

# Convert 'Month' from string (e.g., "January") to number (1–12)
df['Month'] = pd.to_datetime(df['Month'], format='%B').dt.month

# Select input features and target
features = df[[
    'Name of the farmer', 'Type of Soil', 'Type/Variety', 'Location', 'Type of Crops',
    'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Month', 'Year'
]]
target = df['Total']

# One-Hot Encode categorical columns
categorical_cols = ['Name of the farmer', 'Type of Soil', 'Type/Variety', 'Location', 'Type of Crops']
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_cats = encoder.fit_transform(features[categorical_cols])

# Combine encoded categorical with numerical columns
import numpy as np
numerical = features[['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Month', 'Year']].values
X = np.hstack([encoded_cats.toarray(), numerical])

# Train model
model = RandomForestRegressor()
model.fit(X, target)

# Save model and encoder
joblib.dump(model, 'harvest_model.pkl')
joblib.dump(encoder, 'encoder.pkl')

print("✅ Model trained and saved.")
