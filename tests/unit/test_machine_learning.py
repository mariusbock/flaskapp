"""
This file (test_machine_learning.py) contains all unit tests for the model_prediction.py file
"""
import os
from pathlib import Path
from project.machine_learning.model_prediction import *
from project.machine_learning.model_training import *
from project.machine_learning.preprocessing import *
from project.machine_learning.feature_engineering import *



def test_preprocessing():
    dynamic_data = pd.read_csv("static/test_data/raw_data.csv",
                               sep=";", header=0, parse_dates=["timestamp"], index_col=None)
    preprocessed_data = pd.read_csv('static/test_data/preprocessed_data.csv', sep=";",
                                    header=0, parse_dates=['timestamp'], index_col=None).sort_values(
        "timestamp").reset_index(drop=True)

    assert pd.testing.assert_frame_equal(preprocessed_data.reset_index(drop=True),
                                         preprocess_dataset(dynamic_data).reset_index(drop=True),
                                         check_dtype=False,
                                         check_index_type=False) is None


def feature_engineer_dataset():
    preprocessed_data = pd.read_csv('static/test_data/preprocessed_data.csv', parse_dates=["timestamp"], sep=";",
                                    index_col=0)
    feature_engineered_data = pd.read_csv('static/test_data/feature_engineered_data.csv', parse_dates=["timestamp"],
                                          sep=";")

    assert pd.testing.assert_frame_equal(feature_engineered_data.reset_index(drop=True),
                                         feature_engineer_dataset(preprocessed_data).reset_index(drop=True),
                                         check_dtype=False,
                                         check_index_type=False) is None


def test_train_model_occupancy():
    feature_engineered_data = pd.read_csv('static/test_data/feature_engineered_data.csv', parse_dates=["timestamp"],
                                          sep=";")
    response = train_model_occupancy(feature_engineered_data, "LGBM", "test_model.pkl")

    assert Path('test_model.pkl').is_file()
    assert response == "Model successfully trained and saved."

    os.remove('test_model.pkl')
    assert Path('test_model.pkl').is_file() is False
