import pandas as pd
from sqlalchemy import create_engine

from config import Constants

training_db = create_engine(Constants.TRAINING_DATABASE_URI)


def get_all_saved_models():
    try:
        query = "select * from savedmodels"
        data_df = pd.read_sql_query(query, training_db)
        return data_df.to_json(orient="records")
    except:
        raise ValueError("Error trying to retrieve saved models")


def get_all_created_features():
    try:
        query = "select * from createdfeatures"
        data_df = pd.read_sql_query(query, training_db)
        return data_df.to_json(orient="records")
    except:
        raise ValueError("Error trying to retrieve created features")


def save_trained_model_to_db(model):
    try:
        print(model, flush=True)
        query = "INSERT INTO savedmodels VALUES (" + \
                "\'" + model['id'] + "\'" + "," + \
                "\'" + model['name'] + "\'" + "," + \
                "\'" + model['description'] + "\'" + "," + \
                "\'" + model['timestamp'] + "\'" + "," + \
                "\'" + model['clientid'] + "\'" + "," + \
                "\'" + model['requestid'] + "\'" + "," + \
                "\'" + model['downloadlink'] + "\'" + \
                ")"
        print(training_db, flush=True)
        training_db.connect().execute(query)
    except:
        raise ValueError("Error trying to save model to training DB")


def save_created_feature_to_db(model):
    try:
        print(model, flush=True)
        query = "INSERT INTO createdfeatures VALUES (" + \
                "\'" + model['id'] + "\'" + "," + \
                "\'" + model['name'] + "\'" + "," + \
                "\'" + model['description'] + "\'" + "," + \
                "\'" + model['clientid'] + "\'" + "," + \
                "\'" + model['requestid'] + "\'" + "," + \
                "\'" + model['timestamp'] + "\'" + "," + \
                "\'" + model['sqlstatement'] + "\'" + \
                ")"
        print(training_db, flush=True)
        training_db.connect().execute(query)
    except:
        raise ValueError("Error trying to save model to training DB")
