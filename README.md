# F1 Winner Prediction using Linear Regression

[![CI](https://github.com/rmidhun23/f1-winner-prediction/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rmidhun23/f1-winner-prediction/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A machine learning project to predict Formula 1 race winners using historical data and linear regression.

## Approach

- **Algorithm**: Linear Regression
- **Target**: Race winner prediction (binary classification)
- **Data**: Formula 1 races from 2010 onwards

## Features

The model uses 14 features:

- `driver_win_rate` - Historical win rate for the driver (last 25 races)
- `constructor_win_rate` - Historical win rate for the constructor (last 25 races)
- `driver_season_points` - Cumulative points for driver in current season
- `recent_avg_position` - Average finishing position in recent races
- `constructor_recent_wins` - Number of recent wins for the constructor
- `qualifying_position` - Position achieved in qualifying session
- `grid` - Starting grid position for the race
- `num_pit_stops` - Number of pit stops during the race
- `avg_pit_time` - Average pit stop time in milliseconds
- `total_pit_time` - Total pit stop time in milliseconds
- `driver_constructor_interaction` - Interaction term between driver and constructor win rates
- `grid_qualifying_diff` - Difference between grid and qualifying position
- `points_per_race` - Average points per race for the driver
- `year` - Race year (normalized)

## Results

```text
Training MSE: 0.0338
Test MSE: 0.0318

Training R2: 0.2400
Test R2: 0.3346
```

## Data Source

- Kaggle F1 Dataset: [Formula 1 World Championship (1950-2023)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)


## API

- **Health Check**: `GET /health`
- **Predict Winner**: `POST /predict`

## Usage

See individual notebooks for step-by-step analysis and modeling process.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Kaggle account

### 1. Local Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install jupyter ipykernel
python -m ipykernel install --user --name=f1-winner-prediction --display-name="f1-ml"

# Setup pre-commit hooks
pre-commit install

# Download data
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_api_key

python download_data.py

kaggle datasets download \
  -d rohanrao/formula-1-world-championship-1950-2020 \
  -p data/raw/ \
  --unzip
```

### 2. Run Notebooks

```bash
# Start Jupyter
jupyter notebook

# Run in order:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_data_preprocessing.ipynb
# 3. notebooks/03_linear_regression_model.ipynb
```

### 3. Upload to Kaggle

1. Go to Kaggle.com > Datasets > New Dataset
2. Upload the notebooks from `notebooks`folder
3. Set dataset as data source
4. Run and publish

### 4. Run Locally

```bash
# Start server
# Make host to bind to localhost when running locally
python src/api.py

# Test API health
curl -X GET http://localhost:9010/health

# Test API with all features
curl -X POST http://localhost:9010/predict \
  -H "Content-Type: application/json" \
  -d '{
    "drivers": [
      {
        "forename": "Lewis",
        "surname": "Hamilton",
        "driver_win_rate": 0.3,
        "constructor_win_rate": 0.25,
        "driver_season_points": 150.0,
        "qualifying_position": 2,
        "num_pit_stops": 1,
        "avg_pit_time": 25000,
        "total_pit_time": 25000,
        "grid": 2,
        "year": 2024,
        "driver_constructor_interaction": 0.075,
        "grid_qualifying_diff": 0.0,
        "points_per_race": 8.5,
        "recent_avg_position": 3.2,
        "constructor_recent_wins": 2
      }
    ]
  }'
```

## Deployment

### Prerequisites

- [Docker](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Pack](https://buildpacks.io/docs/tools/pack/)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Customize Project Information

Before deploying, update `project.toml`:
- Replace `Name <email@example.com>` with name and email
- Replace `username` with GitHub username

### 1. Local Deployment

```bash
chmod +x deploy.sh
./deploy.sh
```

### 2. Access the API

```bash
# Port forward to access the service locally
kubectl port-forward svc/f1-api-service 9010:9010 -n f1-ml

# Test API (in another terminal)
curl -X POST http://localhost:9010/predict \
  -H "Content-Type: application/json" \
  -d '{
    "drivers": [
      {
        "forename": "Max",
        "surname": "Verstappen",
        "driver_win_rate": 0.45,
        "constructor_win_rate": 0.35,
        "driver_season_points": 220.0,
        "qualifying_position": 1,
        "num_pit_stops": 2,
        "avg_pit_time": 23800,
        "total_pit_time": 47600,
        "grid": 1,
        "year": 2024,
        "driver_constructor_interaction": 0.1575,
        "grid_qualifying_diff": 0.0,
        "points_per_race": 15.2,
        "recent_avg_position": 1.9,
        "constructor_recent_wins": 4
      },
      {
        "forename": "Charles",
        "surname": "Leclerc",
        "driver_win_rate": 0.18,
        "constructor_win_rate": 0.15,
        "driver_season_points": 95.0,
        "qualifying_position": 3,
        "num_pit_stops": 2,
        "avg_pit_time": 26200,
        "total_pit_time": 52400,
        "grid": 4,
        "year": 2024,
        "driver_constructor_interaction": 0.027,
        "grid_qualifying_diff": 1.0,
        "points_per_race": 7.8,
        "recent_avg_position": 4.5,
        "constructor_recent_wins": 1
      },
      {
        "forename": "Lando",
        "surname": "Norris",
        "driver_win_rate": 0.12,
        "constructor_win_rate": 0.08,
        "driver_season_points": 75.0,
        "qualifying_position": 5,
        "num_pit_stops": 1,
        "avg_pit_time": 27500,
        "total_pit_time": 27500,
        "grid": 5,
        "year": 2024,
        "driver_constructor_interaction": 0.0096,
        "grid_qualifying_diff": 0.0,
        "points_per_race": 6.2,
        "recent_avg_position": 6.1,
        "constructor_recent_wins": 0
      }
    ]
  }'
```

### 3. Cleanup

```bash
# Delete the kind cluster
kind delete cluster --name f1-prediction-cluster
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/yourusername/f1-winner-prediction.git
cd f1-winner-prediction

# Setup development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

Thanks to all contributors who have helped improve this project! 🏎️
