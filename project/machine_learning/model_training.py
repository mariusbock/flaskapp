import numpy as np
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error


def train_time_series_model(data, algorithm, timestamp_column, target):
    ordered_data = data.sort_values(timestamp_column)

    # creating the train and validation set
    train = ordered_data[:int(0.8 * (len(ordered_data)))].reset_index().drop("index", axis=1)
    valid = ordered_data[int(0.8 * (len(ordered_data))):].reset_index().drop("index", axis=1)

    # test_request = valid[valid.timestamp == valid['timestamp'].max()].drop(["cars", "occupancy"], axis=1)
    # print(test_request)
    # test_request.to_json("test_request.json", orient="records")
    print(train, flush=True)
    print(valid, flush=True)
    X_train = train.drop(target, axis=1)
    y_train = train[target]
    X_valid = valid.drop(target, axis=1)
    y_valid = valid[target]

    # fit the model
    if algorithm == "LGBM":
        regr = LGBMRegressor(n_estimators=1000, learning_rate=0.01)
        model = regr.fit(X_train, np.log1p(y_train))
    elif algorithm == "RF":
        regr = RandomForestRegressor(n_estimators=1000, n_jobs=-1, verbose=1)
        model = regr.fit(X_train, np.log1p(y_train))

    # make prediction on validation
    prediction = np.expm1(model.predict(X_valid))

    error = rmsle(y_valid, prediction)
    print('Error %.5f' % error, flush=True)

    return model


def rmsle(ytrue, ypred):
    return np.sqrt(mean_squared_log_error(ytrue, ypred))
