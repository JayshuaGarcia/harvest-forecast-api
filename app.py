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

    # Use only the columns expected by the encoder
    encoder_columns = list(encoder.feature_names_in_)
    input_df = input_df[encoder_columns]

    input_encoded = encoder.transform(input_df)
    prediction = model.predict(input_encoded)[0]
    return jsonify({"forecast": round(prediction, 2)})

if __name__ == '__main__':
    app.run(debug=True)
