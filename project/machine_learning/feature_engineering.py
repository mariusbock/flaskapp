from pandasql import sqldf
import pandas as pd
import re
import sqlparse
import itertools


def pysqldf(q):
    return sqldf(q, globals())


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


def create_your_own_feature(sql_statement, training_data):
    """
    Function that takes a create-feature sql statement and applies it to the dataframe to create new columns
    :param sql_statement: create-feature statement written in SQL
    :param training_data: pandas dataframe that the SQL statement is being applied upon
    :return: feature-engineered columns
    """
    # bring SQL statement into correct format for extraction of column names
    parsed_sql = sqlparse.format(sql_statement, keyword_case="upper", identifier_case="lower", strip_comments=True)
    pattern = '[a-z0-9_\.]+'
    involved_columns = list(dict.fromkeys(re.findall(pattern, parsed_sql)))
    column_pairs = []
    for column in involved_columns:
        if len(list(column.split('.'))) > 1:
            column_pairs.append(list(column.split('.')))
        elif not column == "training_data":
            column_pairs.append(list(('trafficoccupancy', column)))
    training_data.columns = map(str.lower, training_data.columns)
    matched_columns = []
    for column_pair in column_pairs:
        if column_pair[0] == "trafficoccupancy":
            matched_columns.append(list(training_data.filter(regex="^"+column_pair[1]).columns.values))
        elif not training_data.filter(regex=column_pair[0]+"(.*)"+column_pair[1]).empty:
            matched_columns.append(list(training_data.filter(regex=column_pair[0]+"(.*)"+column_pair[1]).columns.values))
    sql_query_variants = []
    for combination in itertools.product(*matched_columns):
        final_sql = parsed_sql
        for i in range(len(combination)):
            final_sql = final_sql.replace(involved_columns[i], combination[i])
        sql_query_variants.append(final_sql)
    result_df = pd.DataFrame()
    i = 1
    for sql in sql_query_variants:
        query_result = sqldf(sql, locals())
        for (columnName, columnData) in query_result.iteritems():
            result_df['feature_' + str(i)] = columnData
            i += 1

    print("CREATED FEAUTRE(S):", flush=True)
    print(result_df, flush=True)
    return result_df


if __name__ == '__main__':
    SQL = """select events.occupancy, occupancy from training_data group by events.occupancy;"""
    test_df = pd.DataFrame(data=[("test", "test", "test", "test", "test", "test", "test", "test", "test")],
                           columns=["Events_0_occupancy", "occupancy", "Events_0_DATE_START", "Events_0_VALID_FOR",
                                    "Events_0_type", "Events_0_DATE_END", "Events_0_NAME", "TIMESTAMP", "ROAD_ID"])

    create_your_own_feature(SQL, test_df)
