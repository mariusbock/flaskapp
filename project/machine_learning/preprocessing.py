import datetime
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def start_of_year_time_minutes(dt):
    epoch = datetime.datetime.fromtimestamp(1567296000, tz=dt.tzinfo)  # equivalent to 1.1.2019

    return (dt - epoch).total_seconds() / 60


def label_encode(dataframe):
    # TODO need some sort of list of all IDs (maybe Encoding file) -> First need to clarify issues with Christian
    # roads = pd.read_json("static/parsed_data/roads.json", orient="records")
    print(dataframe.dtypes, flush=True)
    for i in dataframe.columns.values:
        if dataframe[i].dtype == object or "datetime" in str(dataframe[i].dtype):
            le = LabelEncoder()
            dataframe[i] = le.fit_transform(dataframe[i])
    """if type == "timestamp":
        encoded_column = column.apply(start_of_year_time_minutes)
    if type == "road_id":
        # road_list = roads["road_id"].sort_values()
        le.fit(column.sort_values().unique())
        encoded_column = le.transform(column)"""
    return dataframe


# TODO extend by other methods like fill with most frequent value etc.
# TODO may not need categorical and numerical difference (may be beneficial cause in UI it is separated
def fill_missing_values(dataframe, entity_id_columns, timestamp_id_columns, numerical_fill, categorical_fill):
    """
    Fills in missing values in dataset for numerical and categorical
    :param dataframe: initial dataframe
    :param entity_id_columns: identifier columns of entity that you are trying to impute values for
    :param timestamp_id_columns: temporal component of imputation
    :param numerical_fill: pairs of (column_name, fill_method) for numerical columns; column name can be original column name
    :param categorical_fill: pairs of (column_name, fill_method) for categorical columns; column name can be original column name
    :return: dataframe with imputed values
    """
    entity_columns = []
    for entity_column in entity_id_columns:
        entity_columns.extend(dataframe.filter(regex=entity_column).columns.values)

    timestamp_columns = []
    for timestamp_column in timestamp_id_columns:
        timestamp_columns.extend(dataframe.filter(regex=timestamp_column).columns.values)

    numerical_columns = []
    numerical_fill_methods = []
    for numerical_column in numerical_fill:
        numerical_columns.extend(dataframe.filter(regex=numerical_column[0]).columns.values)
        for _ in range(len(dataframe.filter(regex=numerical_column[0]).columns.values)):
            numerical_fill_methods.append(numerical_column[1])

    categorical_columns = []
    categorical_fill_methods = []
    for categorical_column in categorical_fill:
        categorical_columns.extend(dataframe.filter(regex=categorical_column[0]).columns.values)
        for _ in range(len(dataframe.filter(regex=categorical_column[0]).columns.values)):
            categorical_fill_methods.append(categorical_column[1])

    entities = dataframe[entity_columns].drop_duplicates()
    timestamps = dataframe[timestamp_columns].drop_duplicates()
    """
    entities['key'] = 0
    timestamps['key'] = 0
    combined = entities.merge(timestamps, how='outer').drop(columns=['key'])
    df_missing_values = pd.merge(combined, dataframe, on=entity_key)
    """
    df_missing_values = dataframe
    df_imputed_values = pd.DataFrame()
    for index, entity in entities.iterrows():
        temp = df_missing_values
        # Filter out all records concerning one entity
        for column in entity_columns:
            temp = temp[temp[column] == entity[column]]
        i = 0
        for numerical_column in numerical_columns:
            if numerical_fill_methods[i] == "interpolate":
                temp[numerical_column].interpolate(method='linear', inplace=True, limit_direction="both")
            else:
                temp[numerical_column].fillna(numerical_fill_methods[i], inplace=True)
        j = 0
        for categorical_column in categorical_columns:
            if categorical_fill_methods[j] == "most_frequent":
                # TODO: implement this
                pass
            else:
                temp[categorical_column].fillna(categorical_fill_methods[j], inplace=True)

        df_imputed_values = pd.concat([df_imputed_values, temp], axis=0)
    return df_imputed_values


if __name__ == '__main__':
    dynamic_data = pd.read_csv("/Users/mariusbock/git/flaskapp/static/test_data/raw_data.csv",
                               sep=";", header=0, parse_dates=["timestamp"])

    imputed_data = fill_missing_values(dataframe=dynamic_data,
                                       entity_id_columns=["road_id"],
                                       timestamp_id_columns=["timestamp"],
                                       numerical_fill=[],
                                       categorical_fill=[('occupancy', 'test'), ('cars', 'test')]
                                       )
    print(imputed_data)
