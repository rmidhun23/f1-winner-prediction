"""
Utility functions for F1 winner prediction project.
"""

import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_f1_data(data_path="../data/raw/"):
    """Load all F1 datasets."""
    datasets = {}
    files = ["races", "results", "drivers", "constructors", "circuits", "qualifying"]

    for file in files:
        try:
            datasets[file] = pd.read_csv(f"{data_path}{file}.csv")
            print(f"Loaded {file}.csv: {datasets[file].shape}")
        except FileNotFoundError:
            print(f"Warning: {file}.csv not found")

    return datasets


def create_race_features(
    results, races, drivers, constructors, circuits, qualifying=None
):
    """Create comprehensive race dataset with features."""
    # Merge all datasets
    race_data = results.merge(races, on="raceId")
    race_data = race_data.merge(drivers, on="driverId")
    race_data = race_data.merge(constructors, on="constructorId")
    race_data = race_data.merge(circuits, on="circuitId")

    # Add qualifying data if available
    if qualifying is not None:
        qual_pos = (
            qualifying.groupby(["raceId", "driverId"])["position"].first().reset_index()
        )
        qual_pos.columns = ["raceId", "driverId", "qualifying_position"]
        race_data = race_data.merge(qual_pos, on=["raceId", "driverId"], how="left")
        race_data["qualifying_position"] = race_data["qualifying_position"].fillna(
            race_data["grid"]
        )

    return race_data


def calculate_historical_performance(df, window=20):
    """Calculate rolling historical performance metrics."""
    df = df.sort_values(["year", "round"]).copy()

    # Create winner indicator
    df["is_winner"] = (df["position"] == 1).astype(int)

    # Driver historical win rate
    df["driver_win_rate"] = df.groupby("driverId")["is_winner"].transform(
        lambda x: x.rolling(window=window, min_periods=1).mean().shift(1)
    )

    # Constructor historical win rate
    df["constructor_win_rate"] = df.groupby("constructorId")["is_winner"].transform(
        lambda x: x.rolling(window=window, min_periods=1).mean().shift(1)
    )

    # Season points (cumulative)
    df["driver_season_points"] = df.groupby(["driverId", "year"])["points"].transform(
        lambda x: x.expanding().sum().shift(1)
    )

    return df


def prepare_ml_data(race_data, feature_columns, target_column="is_winner"):
    """Prepare data for machine learning."""
    # Select features and target
    ml_data = race_data[
        feature_columns + [target_column, "raceId", "driverId", "year"]
    ].copy()

    # Handle missing values
    ml_data = ml_data.fillna(
        {
            "driver_win_rate": 0,
            "constructor_win_rate": 0,
            "driver_season_points": 0,
            "qualifying_position": 20,
            "grid": 20,
        }
    )

    # Remove remaining missing values
    ml_data = ml_data.dropna()

    return ml_data


def split_train_test(data, train_years_end=2020):
    """Split data into train and test sets by year."""
    train_data = data[data["year"] <= train_years_end].copy()
    test_data = data[data["year"] > train_years_end].copy()

    return train_data, test_data


def scale_features(X_train, X_test):
    """Scale features using StandardScaler."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler


def save_processed_data(
    X_train,
    X_test,
    y_train,
    y_test,
    feature_names,
    scaler,
    test_data,
    output_path="../data/processed/",
):
    """Save all processed data."""
    np.save(f"{output_path}X_train.npy", X_train)
    np.save(f"{output_path}X_test.npy", X_test)
    np.save(f"{output_path}y_train.npy", y_train)
    np.save(f"{output_path}y_test.npy", y_test)

    with open(f"{output_path}feature_names.pkl", "wb") as f:
        pickle.dump(feature_names, f)

    with open(f"{output_path}scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    test_data.to_csv(f"{output_path}test_data_with_ids.csv", index=False)

    print("All processed data saved successfully!")


def evaluate_race_predictions(test_data, predictions):
    """Evaluate model performance on race-by-race basis."""
    test_data = test_data.copy()
    test_data["predicted_win_prob"] = predictions

    race_accuracy = []
    for race_id in test_data["raceId"].unique():
        race_data = test_data[test_data["raceId"] == race_id]

        # Find actual winner
        actual_winner = race_data[race_data["is_winner"] == 1]

        # Find predicted winner (highest probability)
        predicted_winner_idx = race_data["predicted_win_prob"].idxmax()
        predicted_winner = race_data.loc[predicted_winner_idx]

        # Check if prediction is correct
        correct = (
            len(actual_winner) > 0
            and predicted_winner["driverId"] in actual_winner["driverId"].values
        )

        race_accuracy.append(
            {
                "raceId": race_id,
                "correct_prediction": correct,
                "max_prob": race_data["predicted_win_prob"].max(),
            }
        )

    race_accuracy_df = pd.DataFrame(race_accuracy)
    overall_accuracy = race_accuracy_df["correct_prediction"].mean()

    return overall_accuracy, race_accuracy_df
