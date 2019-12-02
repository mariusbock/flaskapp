import pandas as pd
import sys
import numpy as np
import pickle
import datetime

from itertools import product
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_log_error
from sklearn.externals import joblib

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
np.set_printoptions(threshold=sys.maxsize)


# code inspiration: https://machinelearningmastery.com/how-to-develop-machine-learning-models-for-multivariate-multi-step-air-pollution-time-series-forecasting/


def start_of_year_time_minutes(dt):
    epoch = datetime.datetime.fromtimestamp(1567296000, tz=dt.tzinfo) #equivalent to 1.1.2019

    return (dt - epoch).total_seconds()/60


def label_encode(column, type):
    encoded_column = pd.Series()
    # TODO need some sort of list of all IDs (maybe Encoding file) -> First need to clarify issues with Christian
    #roads = pd.read_json("static/parsed_data/roads.json", orient="records")
    le = LabelEncoder()
    if type == "timestamp":
        encoded_column = column.apply(start_of_year_time_minutes)
    if type == "road_id":
        #road_list = roads["road_id"].sort_values()
        le.fit(column.sort_values().unique())
        encoded_column = le.transform(column)

    return encoded_column


def preprocess_dataset(df):
    """
    Preprocessed the data to be in a specific format that is used for ML models
    :param df:
    :return:
    """

    timestamps = df.timestamp.unique()
    road_ids = df.id.unique()
    combined = pd.DataFrame(list(product(timestamps, road_ids)), columns=['timestamp', 'id'])
    df_missing_values = pd.merge(combined, df, on=["timestamp", "id"])
    df_imputed_values = pd.DataFrame()

    for road_id in road_ids:
        temp = df_missing_values[df_missing_values.id == road_id].sort_values("timestamp")
        temp[["occupancy", "cars"]].interpolate(method='linear', inplace=True, limit_direction="both")
        df_imputed_values = pd.concat([df_imputed_values, temp])

    return df_imputed_values


def feature_engineer_dataset(data):
    data['last_occupancy'] = data.groupby(['id'])['occupancy'].shift()
    # data['last_occupancy_diff'] = data.groupby(['id'])['last_occupancy'].diff()
    data['last-1_occupancy'] = data.groupby(['id'])['occupancy'].shift(2)
    # data['last-1_occupancy_diff'] = data.groupby(['id'])['last-1_occupancy'].diff()
    data['last-5_occupancy'] = data.groupby(['id'])['occupancy'].shift(5)
    # data['last-5_occupancy_diff'] = data.groupby(['id'])['last-5_occupancy'].diff()

    data = data.dropna()
    print("\n Feature engineered dataset")
    print(data.head())
    print(data.shape)

    return data


def predict_occupancy(data):
    # TODO: need preprocessing function for new incoming data to make it so that it fits the ML format. Either here or in backend. Probably here.
    # TODO: need better label encoding so that it is consistent here as well

    # Load the model from the file
    model = joblib.load('/models/occupancy_model.pkl')
    processed_data = data.copy()

    prediction = np.expm1(model.predict(processed_data))

    data["occupancy"] = prediction

    return data


def train_model_occupancy(data, algo, filepath):
    # Here feature engineered data is used
    ordered_data = data.sort_values(["timestamp", "id"])

    ordered_data['id'] = label_encode(ordered_data['id'], type="road_id")
    ordered_data['timestamp'] = label_encode(ordered_data['timestamp'], type="timestamp")

    print(ordered_data["id"].value_counts())

    # creating the train and validation set
    train = ordered_data[:int(0.8 * (len(ordered_data)))].reset_index().drop("index", axis=1)
    valid = ordered_data[int(0.8 * (len(ordered_data))):].reset_index().drop("index", axis=1)

    test_request = valid[valid.timestamp == valid['timestamp'].max()].drop(["cars", "occupancy"], axis=1)
    #print(test_request)
    #test_request.to_json("test_request.json", orient="records")

    X_train = train.drop(["cars", "occupancy"], axis=1)
    y_train = train["occupancy"]
    X_valid = valid.drop(["cars", "occupancy"], axis=1)
    y_valid = valid["occupancy"]

    # fit the model
    if algo == "LGBM":
        regr = LGBMRegressor(n_estimators=1000, learning_rate=0.01)
        model = regr.fit(X_train, np.log1p(y_train))
    elif algo == "RF":
        regr = RandomForestRegressor(n_estimators=1000, n_jobs=-1, verbose=1)
        model = regr.fit(X_train, np.log1p(y_train))

    # make prediction on validation
    prediction = np.expm1(model.predict(X_valid))

    error = rmsle(y_valid, prediction)
    print('Error %.5f' % error)

    # Save the model as a pickle in a file
    joblib.dump(model, filepath)

    return "Model successfully trained and saved."


def rmsle(ytrue, ypred):
    return np.sqrt(mean_squared_log_error(ytrue, ypred))


if __name__ == '__main__':
    dynamic_data = pd.read_csv("/Users/mariusbock/git/flaskapp/static/test_data/raw_data.csv",
                               sep=";", header=0, parse_dates=["timestamp"])

    preprocessed_data = preprocess_dataset(dynamic_data)
    preprocessed_data.to_csv("/Users/mariusbock/git/flaskapp/static/test_data/preprocessed_data.csv", sep=";", index=None)
    feature_data = feature_engineer_dataset(preprocessed_data)
    feature_data.to_csv("/Users/mariusbock/git/flaskapp/static/test_data/feature_engineered_data.csv", sep=";", index=None)
    #.to_csv("/Users/mariusbock/git/flaskapp/static/test_data/feature_engineered_data.csv", sep=";", index=None)
    #data = pd.read_json("test_request.json", orient="records")

    #print(data.head())

    #print(predict_occupancy(data))
