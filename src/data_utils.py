"""Utility functions for data processing and validation."""


def validate_race_data(race_data, required_features):
    """
    Validate that race data contains all required features.
    """
    if race_data.empty:
        return False, required_features

    missing_features = [f for f in required_features if f not in race_data.columns]
    is_valid = len(missing_features) == 0

    return is_valid, missing_features


def format_driver_name(driver_data):
    """
    Format driver name from forename and surname.
    """
    forename = driver_data.get("forename", "").strip()
    surname = driver_data.get("surname", "").strip()

    if not forename:
        forename = "Unknown"
    if not surname:
        surname = "Unknown"

    return f"{forename} {surname}"


def calculate_win_probability_stats(predictions):
    """
    Calculate statistics for win probabilities.
    """
    if predictions.empty or "win_probability" not in predictions.columns:
        return {
            "total_drivers": 0,
            "avg_probability": 0,
            "max_probability": 0,
            "min_probability": 0,
        }

    probabilities = predictions["win_probability"]

    return {
        "total_drivers": len(predictions),
        "avg_probability": float(probabilities.mean()),
        "max_probability": float(probabilities.max()),
        "min_probability": float(probabilities.min()),
    }
