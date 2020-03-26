import pandas as pd

from project import training_db


def get_all_saved_models():
    try:
        query = "select * from savedmodels"
        data_df = pd.read_sql_query(query, training_db)
        return data_df.to_json(orient="records")
    except:
        raise ValueError("Error trying to retrieve saved models")


def save_trained_model_to_db(model):
    try:
        print(model, flush=True)
        query = "INSERT INTO savedmodels VALUES (" + "\'" + model['filename'] + "\'" + "," + \
                "\'" + model['timestamp'] + "\'" + "," + \
                "\'" + model['clientid'] + "\'" + "," + \
                "\'" + model['requestid'] + "\'" + "," + \
                "\'" + model['downloadlink'] + "\'" + \
                ")"
        training_db.connect().execute(query)
    except:
        raise ValueError("Error trying to save model to training DB")
