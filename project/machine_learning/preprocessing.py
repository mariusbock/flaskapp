import pandas as pd
from sklearn.preprocessing import LabelEncoder

"""
File that contains all functions to be used for preprocessing
"""


def label_encode(dataframe):
    """
    Function that takes a dataframe and label encodes all non-numeric columns
    :param dataframe: dataframe to be encoded
    :return: encoded dataframe
    """
    # TODO needs to be reworked to have consistent encoding
    # roads = pd.read_json("static/parsed_data/roads.json", orient="records")
    print(dataframe.dtypes, flush=True)
    for i in dataframe.columns.values:
        if dataframe[i].dtype == object or "datetime" in str(dataframe[i].dtype):
            le = LabelEncoder()
            dataframe[i] = le.fit_transform(dataframe[i])

    return dataframe


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
    # first filter dataframe to get all entity, timestamp and columns to be filled
    # TODO should be reworked to be less error prone when there are columns named the same
    # TODO extend by other methods like fill with most frequent value etc.
    # TODO may not need categorical and numerical difference (may be beneficial cause in UI it is separated
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

    # filter dataframe to get list of entities and timestamps
    entities = dataframe[entity_columns].drop_duplicates()
    timestamps = dataframe[timestamp_columns].drop_duplicates()
    """
    entities['key'] = 0
    timestamps['key'] = 0
    combined = entities.merge(timestamps, how='outer').drop(columns=['key'])
    df_missing_values = pd.merge(combined, dataframe, on=entity_key)
    """
    # per entity: filter dataframe to only rows of entity and apply imputation on wanted columns
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
