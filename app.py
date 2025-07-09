from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

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

@app.route('/forecast', methods=['GET'])
def get_forecast():
    df = pd.read_csv('Harvest.csv')
    data = df.to_dict(orient='records')
    return jsonify({"forecast": data})

@app.route('/')
def home():
    return "Harvest Forecast API is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
