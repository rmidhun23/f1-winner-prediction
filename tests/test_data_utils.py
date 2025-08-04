"""Tests for data_utils module."""

from unittest import TestCase

import pandas as pd

from src.data_utils import (
    calculate_win_probability_stats,
    format_driver_name,
    validate_race_data,
)


class TestDataUtils(TestCase):
    """Test cases for data utility functions."""

    def setUp(self):
        """Set up test data."""
        self.valid_race_data = pd.DataFrame(
            {
                "driver_win_rate": [0.3, 0.2, 0.1],
                "constructor_win_rate": [0.25, 0.15, 0.05],
                "qualifying_position": [1, 2, 3],
                "grid": [1, 2, 3],
                "year": [2024, 2024, 2024],
            }
        )

        self.driver_data = pd.DataFrame(
            {
                "forename": ["Lewis", "Max", "Charles"],
                "surname": ["Hamilton", "Verstappen", "Leclerc"],
            }
        )

    def test_validate_race_data_valid(self):
        """Test validation with valid data."""
        required_features = [
            "driver_win_rate",
            "constructor_win_rate",
            "qualifying_position",
        ]

        is_valid, missing = validate_race_data(self.valid_race_data, required_features)

        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    def test_validate_race_data_missing_features(self):
        """Test validation with missing features."""
        required_features = ["driver_win_rate", "missing_feature", "another_missing"]

        is_valid, missing = validate_race_data(self.valid_race_data, required_features)

        self.assertFalse(is_valid)
        self.assertEqual(set(missing), {"missing_feature", "another_missing"})

    def test_validate_race_data_empty_dataframe(self):
        """Test validation with empty DataFrame."""
        empty_df = pd.DataFrame()
        required_features = ["driver_win_rate"]

        is_valid, missing = validate_race_data(empty_df, required_features)

        self.assertFalse(is_valid)
        self.assertEqual(missing, required_features)

    def test_format_driver_name_full_names(self):
        """Test driver name formatting with full names."""
        driver = {"forename": "Lewis", "surname": "Hamilton"}

        formatted = format_driver_name(driver)

        self.assertEqual(formatted, "Lewis Hamilton")

    def test_format_driver_name_missing_forename(self):
        """Test driver name formatting with missing forename."""
        driver = {"surname": "Hamilton"}

        formatted = format_driver_name(driver)

        self.assertEqual(formatted, "Unknown Hamilton")

    def test_format_driver_name_missing_surname(self):
        """Test driver name formatting with missing surname."""
        driver = {"forename": "Lewis"}

        formatted = format_driver_name(driver)

        self.assertEqual(formatted, "Lewis Unknown")

    def test_format_driver_name_both_missing(self):
        """Test driver name formatting with both names missing."""
        driver = {}

        formatted = format_driver_name(driver)

        self.assertEqual(formatted, "Unknown Unknown")

    def test_format_driver_name_empty_strings(self):
        """Test driver name formatting with empty strings."""
        driver = {"forename": "", "surname": ""}

        formatted = format_driver_name(driver)

        self.assertEqual(formatted, "Unknown Unknown")

    def test_calculate_win_probability_stats_basic(self):
        """Test win probability statistics calculation."""
        predictions = pd.DataFrame(
            {
                "driver_name": ["Lewis Hamilton", "Max Verstappen", "Charles Leclerc"],
                "win_probability": [0.6, 0.3, 0.1],
            }
        )

        stats = calculate_win_probability_stats(predictions)

        self.assertIn("total_drivers", stats)
        self.assertIn("avg_probability", stats)
        self.assertIn("max_probability", stats)
        self.assertIn("min_probability", stats)

        self.assertEqual(stats["total_drivers"], 3)
        self.assertAlmostEqual(stats["avg_probability"], 0.333, places=2)
        self.assertEqual(stats["max_probability"], 0.6)
        self.assertEqual(stats["min_probability"], 0.1)

    def test_calculate_win_probability_stats_empty(self):
        """Test win probability statistics with empty data."""
        empty_predictions = pd.DataFrame(columns=["driver_name", "win_probability"])

        stats = calculate_win_probability_stats(empty_predictions)

        self.assertEqual(stats["total_drivers"], 0)
        self.assertEqual(stats["avg_probability"], 0)
        self.assertEqual(stats["max_probability"], 0)
        self.assertEqual(stats["min_probability"], 0)

    def test_calculate_win_probability_stats_single_driver(self):
        """Test win probability statistics with single driver."""
        single_prediction = pd.DataFrame(
            {"driver_name": ["Lewis Hamilton"], "win_probability": [1.0]}
        )

        stats = calculate_win_probability_stats(single_prediction)

        self.assertEqual(stats["total_drivers"], 1)
        self.assertEqual(stats["avg_probability"], 1.0)
        self.assertEqual(stats["max_probability"], 1.0)
        self.assertEqual(stats["min_probability"], 1.0)
