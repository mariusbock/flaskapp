import itertools
import re

import pandas as pd
import sqlparse
from pandasql import sqldf

"""
File that contains all functions used during feature engineering.
"""


def feature_engineer_dataset(data, feature_engineering):
    """
    Older Function that was used to create new features. Needs to be reworked entirely.
    :param data: data to be feature engineered with
    :param feature_engineering: list of wanted feature engineering
    :return: feature engineered dataset
    """
    data['last_occupancy'] = data.groupby(['id'])['occupancy'].shift()
    data['last_occupancy_diff'] = data.groupby(['id'])['last_occupancy'].diff()
    data['last-1_occupancy'] = data.groupby(['id'])['occupancy'].shift(2)
    data['last-1_occupancy_diff'] = data.groupby(['id'])['last-1_occupancy'].diff()
    data['last-5_occupancy'] = data.groupby(['id'])['occupancy'].shift(5)
    data['last-5_occupancy_diff'] = data.groupby(['id'])['last-5_occupancy'].diff()

    data = data.dropna()
    print("\n Feature engineered dataset")
    print(data.head())
    print(data.shape)

    return data


def create_your_own_feature(sql_statement, training_data):
    """
    Function that takes a create-feature sql statement and applies it to the dataframe to create new columns
    :param sql_statement: create-feature statement written in SQL
    :param training_data: pandas dataframe that the SQL statement is being applied upon
    :return: feature-engineered columns
    """
    # bring SQL statement into correct format for extraction of column names
    parsed_sql = sqlparse.format(sql_statement, keyword_case="upper", identifier_case="lower", strip_comments=True)
    # regex over SQL statement to get all columns mentioned within the statement
    pattern = '[a-z0-9_\.]+'
    involved_columns = list(dict.fromkeys(re.findall(pattern, parsed_sql)))

    # for each column mentioned within statement extract the table and attribute name and create a pair
    # save pair to list
    column_pairs = []
    for column in involved_columns:
        if len(list(column.split('.'))) > 1:
            column_pairs.append(list(column.split('.')))
        elif not column == "training_data":
            column_pairs.append(list(('trafficoccupancy', column)))

    # lowercase all column names of training dataframe; iterate over column pairs
    # create list of matches per column pair
    training_data.columns = map(str.lower, training_data.columns)
    matched_columns = []
    for column_pair in column_pairs:
        # if equals query type (trafficoccupancy) regex only for column name (since name won't contain table in training
        # dataframe (see flattening function why this is the case)
        if column_pair[0] == "trafficoccupancy":
            matched_columns.append(list(training_data.filter(regex="^" + column_pair[1]).columns.values))
        # if not query type regex for tablename and column name with any characters inbetween.
        # look at flattening function why this is case
        elif not training_data.filter(regex=column_pair[0] + "(.*)" + column_pair[1]).empty:
            matched_columns.append(
                list(training_data.filter(regex=column_pair[0] + "(.*)" + column_pair[1]).columns.values))
    # create all variants of sql statements by creating all combinations of the lists of matches
    # a combination holds naming variants of the attributes in the training data
    sql_query_variants = []
    for combination in itertools.product(*matched_columns):
        final_sql = parsed_sql
        for i in range(len(combination)):
            # substitute attribute name in sql statement with their naming variant and save statement in list
            final_sql = final_sql.replace(involved_columns[i], combination[i])
        sql_query_variants.append(final_sql)
    result_df = pd.DataFrame()
    i = 1
    # per created statement: apply on dataframe using pandasql and save resulting columns to result dataframe
    for sql in sql_query_variants:
        query_result = sqldf(sql, locals())
        for (columnName, columnData) in query_result.iteritems():
            result_df['feature_' + str(i)] = columnData
            i += 1

    print("CREATED FEAUTRE(S):", flush=True)
    print(result_df, flush=True)
    return result_df
