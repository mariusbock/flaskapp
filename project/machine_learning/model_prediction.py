import sys

import numpy as np
import pandas as pd
from sklearn.externals import joblib

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
np.set_printoptions(threshold=sys.maxsize)

"""
code inspiration: https://machinelearningmastery.com/how-to-develop-machine-learning-models-for-multivariate-multi-step-air-pollution-time-series-forecasting/

"""


def predict_occupancy(data):
    # TODO: need preprocessing function for new incoming data to make it so that it fits the ML format. Either here or in backend. Probably here.
    # TODO: need better label encoding so that it is consistent here as well

    # Load the model from the file
    model = joblib.load('/saved_models/occupancy_model.pkl')
    processed_data = data.copy()

    prediction = np.expm1(model.predict(processed_data))

    data["occupancy"] = prediction

    return data

# if __name__ == '__main__':
# dynamic_data = pd.read_csv("/static/test_data/raw_data.csv",
#                           sep=";", header=0, parse_dates=["timestamp"])

# preprocessed_data = preprocess_dataset(dynamic_data)
# preprocessed_data.to_csv("/Users/mariusbock/git/flaskapp/static/test_data/preprocessed_data.csv", sep=";",
#                         index=None)
# feature_data = feature_engineer_dataset(preprocessed_data)
# feature_data.to_csv("/Users/mariusbock/git/flaskapp/static/test_data/feature_engineered_data.csv", sep=";",
#                    index=None)
# .to_csv("/Users/mariusbock/git/flaskapp/static/test_data/feature_engineered_data.csv", sep=";", index=None)
# data = pd.read_json("test_request.json", orient="records")

# print(data.head())

# print(predict_occupancy(data))
