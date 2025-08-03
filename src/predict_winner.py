"""
Script to make F1 winner predictions using the trained model.
"""

import json
import pickle

import joblib
import pandas as pd


def load_model_and_scalers():
    """
    Load the trained model and scaler.
    """
    import os

    JOB_FILE = "f1_winner_linear_regression.joblib"

    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model = joblib.load(os.path.join(project_root, "models", JOB_FILE))

    with open(
        os.path.join(project_root, "data", "processed", "scalers.pkl"), "rb"
    ) as f:
        scalers = pickle.load(f)

    with open(os.path.join(project_root, "data", "processed", "metadata.json")) as f:
        metadata = json.load(f)

    return model, scalers, metadata["feature_names"]


def predict_race_winner(race_data, model, scalers, original_data=None):
    """
    Predict race winner from race data using mixed scaling strategy.
    """
    race_data_scaled = race_data.copy()

    # Apply mixed scaling strategy
    for feature, scaler in scalers.items():
        if feature in race_data_scaled.columns:
            race_data_scaled[feature] = scaler.transform(race_data_scaled[[feature]])

    # Make predictions
    predictions = model.predict(race_data_scaled)

    # Use original data if provided, otherwise use race_data
    result_data = (
        original_data.copy() if original_data is not None else race_data.copy()
    )
    result_data["win_probability"] = predictions.flatten()

    # Find most likely winner
    winner_idx = result_data["win_probability"].idxmax()
    predicted_winner = result_data.loc[winner_idx]

    return result_data.sort_values("win_probability", ascending=False), predicted_winner


def example_prediction():
    """
    Example of how to use the prediction function.
    """
    # Load model
    model, scalers, feature_names = load_model_and_scalers()

    # Example race data
    example_race = pd.DataFrame(
        {
            "constructor_win_rate": [0.30, 0.20, 0.15, 0.10, 0.05],
            "constructor_recent_wins": [0.333333, 0.0, 0.0, 0.0, 0.0],
            "driver_win_rate": [0.25, 0.15, 0.10, 0.05, 0.02],
            "grid": [0.333333, 0.500000, 0.666667, 0.166667, 0.541667],
            "qualifying_position": [0.125000, 0.166667, 0.041667, 0.208333, 0.083333],
            "driver_constructor_interaction": [0.0, 0.333333, 0.0, 0.0012, 0.0],
            "num_pit_stops": [1, 2, 1, 1, 1],
            "points_per_race": [0.689655, 0.344828, 0.172414, 0.0, -0.344828],
            "recent_avg_position": [0.305556, 0.583333, 0.805556, -0.388889, -0.805556],
            "year": [2024, 2024, 2024, 2024, 2024],
            "grid_qualifying_diff": [0.958333, 0.625000, 0.375000, 0.916667, 0.958333],
            "driver_season_points": [150, 120, 80, 60, 40],
            "driver_name": ["Driver A", "Driver B", "Driver C", "Driver D", "Driver E"],
            "avg_pit_time": [
                21791.600000,
                24132.333333,
                22487.000000,
                25619.500000,
                22210.000000,
            ],
            "total_pit_time": [108958, 72397, 22487, 51239, 44420],
        }
    )

    # Make prediction
    predictions, winner = predict_race_winner(
        example_race[feature_names], model, scalers, example_race
    )

    print("Race Predictions (sorted by win probability):")
    print(predictions[["driver_name", "win_probability"]].head())

    print("")
    print(
        f"Predicted Winner: {winner['driver_name']} (Probability: {winner['win_probability']:.3f})"
    )


if __name__ == "__main__":
    example_prediction()
