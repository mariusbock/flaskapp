import json
import time

import pandas as pd
from flatten_json import flatten

from project.celery import celery
from project.machine_learning.model_training import train_time_series_model
from project.machine_learning.preprocessing import fill_missing_values, label_encode

pd.set_option('display.expand_frame_repr', False)

"""
File that contains all functionalities (wrappers) of Celery instance
"""


@celery.task
def test_bg_job():
    """
    Sample Background task used for testing.
    :return: Status message
    """
    print("THIS STRING WAS PRINTED FROM A BACKGROUND JOB")
    return "Simple Background Job test Successful. Look on the server log to see if a message was printed"


@celery.task(bind=True, track_started=True)
def test_complex_bg_job(self):
    """
    Sample complex background task with multiple stages.
    :return: Status message
    """
    print("INITIATED BG JOB...\n")
    status_int = 0
    status = "INITIALIZED"
    for i in range(10):
        print("NEW ITERATION...\n")
        if (status_int < 2):
            status = "INITIALIZED"

        elif (status_int >= 2 or status_int < 6):
            status = "PREPROCESSING"

        elif (status_int >= 6 or status_int <= 9):
            status = "COMPUTATING"

        else:
            status = "FINISHED"

        self.update_state(state=status, meta={'current': status_int, 'status': status_int})
        time.sleep(5)
        status_int += 1

    return {'current': 100, 'status': 'Task completed!', 'result': 42}


@celery.task(bind=True)
def process_train_request(self, request):
    """
    Wrapper that handles a train request by server by going through all stages of training process using information
    from request.
    :param self:
    :param request: train request send by client that contains all information for model training
    """
    current_step = 0
    total_steps = 4  # the number of suboperations in a task, used for displaying a progress in percent -> more steps = change this int!

    """
    current_step += 1
    self.update_state(state="SEARCHING FOR REQUEST",
                      meta={'request_id': request['request_id'], 'client_id': request.client_id,
                            'progress': (current_step / total_steps) * 100})
    request = search_if_exists_already(request)
    notify_java_server(request, newStatus="SEARCHING FOR REQUEST")

    current_step += 1
    self.update_state(state="PERSISTING THE DATA",
                      meta={'request_id': request.request_id, 'client_id': request.client_id,
                            'progress': (current_step / total_steps) * 100})
    request = persist_data(request)
    notify_java_server(request, newStatus="PERSISTING THE DATA")
    """

    current_step += 1
    self.update_state(state="PREPROCESSING THE DATA",
                      meta={'request_id': request['requestId'], 'client_id': request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    request = preprocess_data(request)
    notify_java_server(request, newStatus="PREPROCESSING THE DATA")

    current_step += 1
    """self.update_state(state="FEATURE ENGINEERING THE DATA",
                      meta={'request_id': request['requestId'], 'client_id': request['clientId'],
                            'progress': (current_step / total_steps) * 100})"""
    request = feature_engineer_data(request)
    notify_java_server(request, newStatus="FEATURE ENGINEERING THE DATA")

    current_step += 1
    """self.update_state(state="ENCODING THE DATA",
                      meta={'request_id': request['requestId'], 'client_id': request['clientId'],
                            'progress': (current_step / total_steps) * 100})"""
    request = encode_data(request)
    notify_java_server(request, newStatus="ENCODING THE DATA")

    current_step += 1
    """self.update_state(state="TRAINING THE MODEL",
                      meta={'request_id': request['requestId'], 'client_id': request['clientId'],
                            'progress': (current_step / total_steps) * 100})"""
    request = train_model(request)
    notify_java_server(request, newStatus="TRAINING THE MODEL")

    """
    current_step += 1
    self.update_state(state="PERSISTING THE RESULT",
                      meta={'request_id': request.request_id, 'client_id': request.client_id,
                            'progress': (current_step / total_steps) * 100})
    request = persist_result(request)
    notify_java_server(request, newStatus="PERSISTING THE RESULT")
    """

def notify_java_server(request, newStatus):
    """
    Function that calls an endpoint from java server that updates the cached status of the request.
    :param request: request who's status wants to be updated
    :param newStatus: new status of the request
    :return:
    """
    print(newStatus)
    pass


# Mock Functions that describe the workflow
# TODO implement functions
def search_if_exists_already(request):
    pass


def persist_data(request):
    pass


def preprocess_data(request):
    flattened_json = pd.DataFrame(flatten(record) for record in request["data"]['TrafficOccupancy'])
    imputed_dataframe = fill_missing_values(dataframe=flattened_json,
                                            entity_id_columns=["ROAD_ID"],
                                            timestamp_id_columns=["TIMESTAMP"],
                                            numerical_fill=[('occupancy', 'interpolate')],
                                            categorical_fill=[]
                                            )
    output_json = imputed_dataframe.to_json(index=False, orient='table')
    request["data"] = output_json
    return request


def feature_engineer_data(request):
    return request


def encode_data(request):
    unencoded_data = pd.read_json(request["data"], orient='table')
    request['data'] = label_encode(unencoded_data).to_json(index=False, orient='table')
    return request


def train_model(request):
    full_data = pd.read_json(request['data'], orient='table')
    request['data'] = train_time_series_model(data=full_data,
                                              algorithm="LGBM",
                                              entity_columns=["ROAD_ID"],
                                              timestamp_column=["TIMESTAMP"],
                                              target=["occupancy"],
                                              filepath="../saved_models/test.pkl"
                                              )
    return request


def predict_occupancy(request):
    pass


def persist_result(request):
    pass


"""if __name__ == '__main__':
    with open("/Users/mariusbock/git/flaskapp/static/test_data/test_flask_request.json") as f:
        request = json.load(f)
    request = preprocess_data(request)
    request = encode_data(request)
    request = train_model(request)"""
