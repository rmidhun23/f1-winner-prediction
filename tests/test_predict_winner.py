"""Tests for predict_winner module."""

import unittest.mock as mock
from unittest import TestCase

import pandas as pd
from sklearn.linear_model import LinearRegression

from src.predict_winner import (
    example_prediction,
    load_model_and_scalers,
    predict_race_winner,
)


class TestPredictWinner(TestCase):
    """Test cases for prediction functions."""

    def setUp(self):
        """Set up test data."""
        self.sample_race_data = pd.DataFrame(
            {
                "driver_win_rate": [0.3, 0.2],
                "constructor_win_rate": [0.25, 0.15],
                "qualifying_position": [1, 2],
                "grid": [1, 2],
                "year": [2024, 2024],
            }
        )

        self.sample_original_data = pd.DataFrame(
            {
                "forename": ["Lewis", "Max"],
                "surname": ["Hamilton", "Verstappen"],
                "driver_win_rate": [0.3, 0.2],
                "constructor_win_rate": [0.25, 0.15],
            }
        )

    def test_predict_race_winner_basic(self):
        """Test basic prediction functionality."""
        # Mock model and scalers
        mock_model = mock.MagicMock()
        mock_model.predict.return_value = [[0.7], [0.3]]

        mock_scalers = {
            "driver_win_rate": mock.MagicMock(),
            "constructor_win_rate": mock.MagicMock(),
        }

        # Configure scalers to return input unchanged
        for scaler in mock_scalers.values():
            scaler.transform.return_value = [[0.3], [0.2]]  # Match input size

        predictions, winner = predict_race_winner(
            self.sample_race_data, mock_model, mock_scalers, self.sample_original_data
        )

        # Verify predictions
        self.assertIsInstance(predictions, pd.DataFrame)
        self.assertIn("win_probability", predictions.columns)
        self.assertEqual(len(predictions), 2)

        # Verify winner selection
        self.assertIsInstance(winner, pd.Series)
        self.assertEqual(winner["win_probability"], 0.7)

    def test_predict_race_winner_without_original_data(self):
        """Test prediction without original data."""
        mock_model = mock.MagicMock()
        mock_model.predict.return_value = [[0.6], [0.4]]

        mock_scalers = {}

        predictions, winner = predict_race_winner(
            self.sample_race_data, mock_model, mock_scalers
        )

        self.assertIsInstance(predictions, pd.DataFrame)
        self.assertIn("win_probability", predictions.columns)

    @mock.patch("os.path.dirname")
    @mock.patch("os.path.abspath")
    @mock.patch("joblib.load")
    @mock.patch("builtins.open")
    @mock.patch("pickle.load")
    @mock.patch("json.load")
    def test_load_model_and_scalers(
        self, mock_json, mock_pickle, mock_open, mock_joblib, mock_abspath, mock_dirname
    ):
        """Test model and scalers loading."""
        # Mock file paths
        mock_dirname.return_value = "/project"
        mock_abspath.return_value = "/project/src/predict_winner.py"

        # Mock model
        mock_model = LinearRegression()
        mock_joblib.return_value = mock_model

        # Mock scalers
        mock_scalers = {"feature1": mock.MagicMock()}
        mock_pickle.return_value = mock_scalers

        # Mock metadata
        mock_metadata = {"feature_names": ["feature1", "feature2"]}
        mock_json.return_value = mock_metadata

        model, scalers, feature_names = load_model_and_scalers()

        self.assertEqual(model, mock_model)
        self.assertEqual(scalers, mock_scalers)
        self.assertEqual(feature_names, ["feature1", "feature2"])

    @mock.patch("src.predict_winner.load_model_and_scalers")
    @mock.patch("src.predict_winner.predict_race_winner")
    def test_example_prediction(self, mock_predict, mock_load):
        """Test example prediction function."""
        # Mock loaded components
        mock_model = mock.MagicMock()
        mock_scalers = {}
        mock_features = ["driver_win_rate", "constructor_win_rate"]
        mock_load.return_value = (mock_model, mock_scalers, mock_features)

        # Mock prediction results
        mock_predictions = pd.DataFrame(
            {"driver_name": ["Driver A", "Driver B"], "win_probability": [0.6, 0.4]}
        )
        mock_winner = {"driver_name": "Driver A", "win_probability": 0.6}
        mock_predict.return_value = (mock_predictions, mock_winner)

        # Should not raise any exceptions
        example_prediction()

        # Verify functions were called
        mock_load.assert_called_once()
        mock_predict.assert_called_once()

    def test_predict_race_winner_scaling(self):
        """Test that scaling is applied correctly."""
        mock_model = mock.MagicMock()
        mock_model.predict.return_value = [[0.5], [0.5]]

        # Mock scaler that doubles values
        mock_scaler = mock.MagicMock()
        mock_scaler.transform.return_value = [[0.6], [0.4]]  # Match input size

        mock_scalers = {"driver_win_rate": mock_scaler}

        predict_race_winner(self.sample_race_data, mock_model, mock_scalers)

        # Verify scaler was called
        mock_scaler.transform.assert_called()

    def test_predict_race_winner_sorting(self):
        """Test that predictions are sorted by probability."""
        mock_model = mock.MagicMock()
        mock_model.predict.return_value = [[0.3], [0.7]]  # Second driver higher

        mock_scalers = {}

        predictions, winner = predict_race_winner(
            self.sample_race_data, mock_model, mock_scalers
        )

        # Verify sorting (highest probability first)
        probabilities = predictions["win_probability"].tolist()
        self.assertEqual(probabilities, [0.7, 0.3])

        # Verify winner is highest probability
        self.assertEqual(winner["win_probability"], 0.7)
