#!/usr/bin/env python3

"""
Download data from Kaggle
This is a utility function to download dataset from Kaggle
"""

import os

from kaggle.api.kaggle_api_extended import KaggleApi


def download_data():
    """
    This function downloads the dataset from Kaggle and extracts it to the data/raw directory.
    It also lists the downloaded files and returns True if the download is successful.
    """

    # Check if environment variables are set
    if not os.environ.get("KAGGLE_USERNAME") or not os.environ.get("KAGGLE_KEY"):
        print("Please set KAGGLE_USERNAME and KAGGLE_KEY environment variables")
        return False

    # Initialize Kaggle API
    api = KaggleApi()

    api.authenticate()

    # Create data directory
    os.makedirs("data/raw", exist_ok=True)

    # Download dataset
    print("Downloading dataset...")

    api.dataset_download_files(
        "rohanrao/formula-1-world-championship-1950-2020", path="data/raw/", unzip=True
    )

    print("Dataset downloaded and extracted to data/raw/")

    # List downloaded files
    raw_files = os.listdir("data/raw")
    print(f"Downloaded files: {raw_files}")

    return True


if __name__ == "__main__":
    success = download_data()

    if success:
        print("\nData download complete!")
    else:
        print("\nData download failed!")
