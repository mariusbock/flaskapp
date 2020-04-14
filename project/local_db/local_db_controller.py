import pandas as pd
from flask import make_response, jsonify
from sqlalchemy.orm import sessionmaker

from project.local_db.models import *

"""
File that contains all functions used for interacting with local database
"""

Session = sessionmaker(bind=local_db.engine)


def save_train_request_to_db(request):
    """
    Function to save train request to database
    :param request: request to be saved to DB
    """
    session = Session()
    session.add(request)
    session.commit()


def get_train_request_by_id(request_id):
    """
    Get train request record via ID
    :param request_id: request ID of train request
    :return: data record of train request
    """
    try:
        query = "SELECT * FROM TrainRequest WHERE TrainRequest.request_id=" + "\'" + request_id + "\'"
        data_df = pd.read_sql_query(query, local_db.engine)
        return make_response(data_df.to_json(orient='records'), 200)
    except:
        raise ValueError("Not a valid requestId")


def get_table_from_db(table):
    """
    Function to get table from DB
    :param table: wanted table
    :return: all records from that table
    """
    try:
        query = "SELECT * FROM " + "\''" + table + "\''"
        data_df = pd.read_sql_query(query, local_db.engine)
        return make_response(data_df.to_json(orient='records'), 200)
    except:
        raise ValueError("Data could not be retrieved.")


def count_entries_in_table_per_id():
    """
    Function to return count of entries in train data database grouped by ID
    :return: count of records grouped by ID of train data table
    """
    try:
        query = "SELECT count(TrainData.id) FROM TrainData GROUP BY TrainData.timestamp"
        data_df = pd.read_sql_query(query, local_db.engine)
        return make_response(data_df.to_json(orient='records'), 200)
    except:
        raise ValueError("Error counting entries from table")


def delete_old_entries_from_table(fields):
    """
    Function to delete old entries from database
    :param fields: fields to be deleted
    """
    try:
        # TODO write function that deletes certain fields
        pass
    except:
        raise ValueError("Error deleting entries from table")


def check_missing_data():
    """
    Function to check whether there is missing data in the DB
    """
    try:
        # TODO write function that checks for missing data
        pass
    except:
        raise ValueError("Error checking for missing data.")


def send_response_to_server():
    """
    Function that checks if there is missing data if so then database is refreshed
    :return:
    """
    result = check_missing_data()
    if result:
        ok_response = {'message': 'true', 'code': 'SUCCESS'}
        print("ALL DATA IS AVAILABLE")
        return make_response(jsonify(ok_response), 200)
    else:
        bad_response = {'message': 'false', 'code': 'CONFLICT'}
        print("DATA IS MISSING")
        # TODO call function that refresh data in DB

        return make_response(jsonify(bad_response), 409)
