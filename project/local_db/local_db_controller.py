import pandas as pd
from flask import make_response, jsonify
from sqlalchemy.orm import sessionmaker

from project.local_db.models import *

Session = sessionmaker(bind=local_db.engine)


def save_request_to_db(request):
    session = Session()
    session.add(request)
    session.commit()


def get_request_by_id(request_id):
    """if not local_db.engine.dialect.has_table(local_db.engine, "requests"):  # If table don't exist, Create.
        print("CREATING TABLE\n")
        metadata = MetaData(local_db.engine)
        # Create a table with the appropriate Columns
        Table("requests", metadata,
              Column('request_id', String, primary_key=True, nullable=False),
              Column('client_id', String),
              Column('raw_data', String),
              Column('meta_data', String),
              Column('request_status', String))
        # Implement the creation
        metadata.create_all()"""
    try:
        query = "SELECT * FROM TrainRequest WHERE TrainRequest.request_id=" + "\'" + request_id + "\'"
        data_df = pd.read_sql_query(query, local_db.engine)
        return make_response(data_df.to_json(orient='records'), 200)
    except:
        raise ValueError("Not a valid requestId")


def get_table_from_db(table):
    try:
        query = "SELECT * FROM " + "\''" + table + "\''"
        data_df = pd.read_sql_query(query, local_db.engine)
        return make_response(data_df.to_json(orient='records'), 200)
    except:
        raise ValueError("Data could not be retrieved.")


def count_entries_in_table_per_id():
    try:
        query = "SELECT count(TrainData.id) FROM TrainData GROUP BY TrainData.timestamp"
        data_df = pd.read_sql_query(query, local_db.engine)
        return make_response(data_df.to_json(orient='records'), 200)
    except:
        raise ValueError("Error counting entries from table")


def delete_old_entries_from_table(fields):
    try:
        # TODO write function that deletes certain fields
        pass
    except:
        raise ValueError("Error deleting entries from table")


def check_missing_data():
    try:
        # TODO write function that checks for missing data
        pass
    except:
        raise ValueError("Error checking for missing data.")


def send_response_to_server():
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
