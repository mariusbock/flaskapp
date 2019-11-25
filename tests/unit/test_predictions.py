"""
This file (test_predictions.py) contains all unit tests for the predictions.py file
"""
from project.predictions import *


def test_preprocessing():
    dynamic_data = pd.read_csv("static/test_data/raw_data.csv",
                               sep=";", header=0, parse_dates=["timestamp"])
    preprocessed_data = pd.read_csv('static/test_data/preprocessed_data.csv', sep=";", header=0, parse_dates=['timestamp'], index_col=0)

    assert preprocessed_data.equals(preprocess_dataset(dynamic_data))


def feature_engineer_dataset():
    preprocessed_data = pd.read_csv('static/test_data/preprocessed_data.csv', parse_dates=["timestamp"])
    feature_engineered_data = pd.read_csv('static/test_data/preprocessed_data.csv', parse_dates=["timestamp"])

    assert feature_engineered_data.equals(feature_engineer_dataset(preprocessed_data))


def test_train_model_occupancy():
    preprocessed_data = pd.read_csv('static/test_data/preprocessed_data.csv', parse_dates=["timestamp"])
    response = train_model_occupancy(preprocessed_data)

    assert response == "Model is trained and saved as Pickle"
