"""
REST API for F1 winner predictions.
"""

import logging

import pandas as pd
from flask import Flask, jsonify, request

from predict_winner import load_model_and_scalers, predict_race_winner

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load model once at startup
try:
    model, scalers, feature_names = load_model_and_scalers()
    app.logger.info("Model loaded successfully")
except Exception as e:
    app.logger.error(f"Failed to load model: {e}")
    model, scalers, feature_names = None, None, None


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "model_loaded": model is not None})


@app.route("/predict", methods=["POST"])
def predict():
    """Predict race winner from JSON data."""
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()
        if not data or "drivers" not in data:
            return jsonify({"error": "Invalid input: 'drivers' field required"}), 400

        # Convert to DataFrame
        race_data = pd.DataFrame(data["drivers"])

        # Validate required features
        missing_features = [f for f in feature_names if f not in race_data.columns]
        if missing_features:
            return jsonify({"error": f"Missing features: {missing_features}"}), 400

        # Make prediction
        predictions, winner = predict_race_winner(
            race_data[feature_names], model, scalers, race_data
        )

        # Format response
        result = {
            "predicted_winner": {
                "full_name": winner.get("forename", "Unknown")
                + winner.get("surname", "Unknown"),
                "win_probability": float(winner["win_probability"]),
            },
            "all_predictions": [
                {
                    "full_name": row.get("forename", "Unknown")
                    + row.get("surname", "Unknown"),
                    "win_probability": float(row["win_probability"]),
                }
                for _, row in predictions.iterrows()
            ],
        }

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9010)
    # app.run(host='127.0.0.1', port=9010)   # Local only
