import pandas as pd
from sqlalchemy import create_engine

from config import Constants

"""
File that contains all functions to interact with training database.
"""

# connection object to training DB; used to interact with training DB
training_db = create_engine(Constants.TRAINING_DATABASE_URI)


def get_all_saved_models():
    """
    Function that returns all saved models stored in training database. NOTE: should be omitted in future iterations
    since direct link to training DB not wanted - do via GraphQL endpoint of xData
    :return: list of saved models as JSON
    """
    try:
        query = "select * from savedmodels"
        data_df = pd.read_sql_query(query, training_db)
        return data_df.to_json(orient="records")
    except:
        raise ValueError("Error trying to retrieve saved models")


def get_all_created_features():
    """
    Function that returns all created features stored in training database. NOTE: should be omitted in future iterations
    since direct link to training DB not wanted - do via GraphQL endpoint of xData
    :return: list of created features as JSON
    """
    try:
        query = "select * from createdfeatures"
        data_df = pd.read_sql_query(query, training_db)
        return data_df.to_json(orient="records")
    except:
        raise ValueError("Error trying to retrieve created features")


def save_trained_model_to_db(model):
    """
    Function that saves trained model to training database. NOTE: should be omitted in future iterations
    since direct link to training DB not wanted - do via GraphQL endpoint of xData
    :param model: model record to be saved
    :return: response
    """
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


def save_created_feature_to_db(created_feature):
    """
    Function that saves created feature to training database. NOTE: should be omitted in future iterations
    since direct link to training DB not wanted - do via GraphQL endpoint of xData
    :param created_feature: created_feature record to be saved
    :return: response
    """
    try:
        print(created_feature, flush=True)
        query = "INSERT INTO createdfeatures VALUES (" + \
                "\'" + created_feature['id'] + "\'" + "," + \
                "\'" + created_feature['name'] + "\'" + "," + \
                "\'" + created_feature['description'] + "\'" + "," + \
                "\'" + created_feature['clientid'] + "\'" + "," + \
                "\'" + created_feature['requestid'] + "\'" + "," + \
                "\'" + created_feature['timestamp'] + "\'" + "," + \
                "\'" + created_feature['sqlstatement'] + "\'" + \
                ")"
        print(training_db, flush=True)
        training_db.connect().execute(query)
    except:
        raise ValueError("Error trying to save model to training DB")
