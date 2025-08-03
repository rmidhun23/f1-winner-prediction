"""Tests for API module."""

import json
import unittest.mock as mock
from unittest import TestCase

import pandas as pd

from src.api import app


class TestAPI(TestCase):
    """Test cases for Flask API."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("status", data)
        self.assertIn("model_loaded", data)
        self.assertEqual(data["status"], "healthy")

    @mock.patch("src.api.model", None)
    def test_health_endpoint_no_model(self):
        """Test health endpoint when model is not loaded."""
        response = self.app.get("/health")
        data = json.loads(response.data)
        self.assertFalse(data["model_loaded"])

    @mock.patch("src.api.model", None)
    def test_predict_no_model(self):
        """Test predict endpoint when model is not loaded."""
        response = self.app.post("/predict", json={"drivers": []})
        self.assertEqual(response.status_code, 500)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "Model not loaded")

    def test_predict_invalid_input(self):
        """Test predict endpoint with invalid input."""
        # No drivers field
        response = self.app.post("/predict", json={})
        self.assertEqual(response.status_code, 400)

        # Empty request
        response = self.app.post("/predict", data="", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @mock.patch("src.api.predict_race_winner")
    @mock.patch("src.api.model", mock.MagicMock())
    @mock.patch("src.api.scalers", {})
    @mock.patch("src.api.feature_names", ["driver_win_rate", "constructor_win_rate"])
    def test_predict_success(self, mock_predict):
        """Test successful prediction."""
        # Mock prediction results
        mock_predictions = pd.DataFrame(
            {
                "forename": ["Lewis", "Max"],
                "surname": ["Hamilton", "Verstappen"],
                "win_probability": [0.7, 0.3],
            }
        )
        mock_winner = {
            "forename": "Lewis",
            "surname": "Hamilton",
            "win_probability": 0.7,
        }
        mock_predict.return_value = (mock_predictions, mock_winner)

        test_data = {
            "drivers": [
                {
                    "forename": "Lewis",
                    "surname": "Hamilton",
                    "driver_win_rate": 0.3,
                    "constructor_win_rate": 0.25,
                }
            ]
        }

        response = self.app.post("/predict", json=test_data)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("predicted_winner", data)
        self.assertIn("all_predictions", data)

    def test_predict_missing_features(self):
        """Test predict endpoint with missing features."""
        with (
            mock.patch("src.api.model", mock.MagicMock()),
            mock.patch("src.api.feature_names", ["required_feature"]),
        ):
            test_data = {"drivers": [{"forename": "Lewis", "surname": "Hamilton"}]}

            response = self.app.post("/predict", json=test_data)
            self.assertEqual(response.status_code, 400)

            data = json.loads(response.data)
            self.assertIn("Missing features", data["error"])
