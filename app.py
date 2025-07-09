from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("harvest_model.pkl")
encoder = joblib.load("encoder.pkl")

@app.route('/forecast', methods=['POST'])
def forecast():
    data = request.json

    input_df = pd.DataFrame([data])
    input_df['Month'] = pd.to_datetime(input_df['Month'], format='%B').dt.month

    encoder_columns = list(encoder.feature_names_in_)
    input_df = input_df[encoder_columns]

    input_encoded = encoder.transform(input_df)
    prediction = model.predict(input_encoded)[0]
    return jsonify({"forecast": round(prediction, 2)})

# THIS IS THE CRITICAL PART:
@app.route('/forecast', methods=['GET'])
def get_forecast():
    data = {
        "forecast": [
            {"crop": "rice", "year": 2026, "yield": 602},
            {"crop": "corn", "year": 2026, "yield": 504},
            {"crop": "vegetables", "year": 2026, "yield": 417},
            {"crop": "fruits", "year": 2026, "yield": 266}
        ]
    }
    return jsonify(data)

@app.route('/')
def home():
    return "Harvest Forecast API is running!"

if __name__ == '__main__':
    app.run(debug=True)
