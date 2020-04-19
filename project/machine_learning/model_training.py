import numpy as np
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error

"""
File that contains all functions used to train models
"""


def train_time_series_model(data, algorithm, timestamp_column, target):
    """
    Function used to train a time series model. Can be more extended with more parameter options.
    :param data: data to be used for training
    :param algorithm: machine learing algorithm to be used for training
    :param timestamp_column: timestamp column of the time series data
    :param target: target to be predicted in the time series
    :return: trained model
    """
    ordered_data = data.sort_values(timestamp_column)

    # creating the train and validation set
    train = ordered_data[:int(0.8 * (len(ordered_data)))].reset_index().drop("index", axis=1)
    valid = ordered_data[int(0.8 * (len(ordered_data))):].reset_index().drop("index", axis=1)

    x_train = train.drop(target, axis=1)
    y_train = train[target]
    x_valid = valid.drop(target, axis=1)
    y_valid = valid[target]

    # fit the model
    if algorithm == "LGBM":
        regressor = LGBMRegressor(n_estimators=1000, learning_rate=0.01)
        model = regressor.fit(x_train, np.log1p(y_train))
    elif algorithm == "RF":
        regressor = RandomForestRegressor(n_estimators=1000, n_jobs=-1, verbose=1)
        model = regressor.fit(x_train, np.log1p(y_train))

    # make prediction on validation
    prediction = np.expm1(model.predict(x_valid))

    error = rmsle(y_valid, prediction)
    print('Error %.5f' % error, flush=True)

    return model


def rmsle(ytrue, ypred):
    """
    Function to calculate Root Mean Squared Logarithmic Error (RMSLE)
    :param ytrue: true label
    :param ypred: predicted label
    :return: RMSLE
    """
    return np.sqrt(mean_squared_log_error(ytrue, ypred))
