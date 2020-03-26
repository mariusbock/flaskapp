import json
import os
import pandas as pd
import requests
import time
from sklearn.externals import joblib
from flatten_json import flatten

from project.celery import celery
from project.machine_learning.model_training import train_time_series_model
from project.machine_learning.preprocessing import fill_missing_values, label_encode
from config import Constants
from project.training_db.training_db_cotroller import save_trained_model_to_db

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


@celery.task(bind=True, track_started=True)
def process_train_request(self, train_request):
    """
    Wrapper that handles a train train_request by server by going through all stages of training process using information
    from train_request.
    :param train_request: train train_request send by client that contains all information for model training
    :param self: celery object
    """
    current_step = 0
    # number of suboperations in a task, used for displaying a progress in percent -> more steps = change this int!
    total_steps = 5
    ##### TRAINING STARTED #####
    train_request = notify_java_server(train_request, new_status="TRAINING JOB STARTED",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="TRAINING JOB STARTED",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    """
    notify_java_server(train_request, new_status="SEARCHING FOR REQUEST")
    current_step += 1
    self.update_state(state="SEARCHING FOR REQUEST",
                      meta={'request_id': train_request['request_id'], 'client_id': train_request.client_id,
                            'progress': (current_step / total_steps) * 100})
    train_request = search_if_exists_already(train_request)

    notify_java_server(train_request, new_status="PERSISTING THE DATA")
    current_step += 1
    self.update_state(state="PERSISTING THE DATA",
                      meta={'request_id': train_request.request_id, 'client_id': train_request.client_id,
                            'progress': (current_step / total_steps) * 100})
    train_request = persist_data(train_request)
    """
    ##### PREPROCESSING #####
    train_request = notify_java_server(train_request, new_status="PREPROCESSING THE DATA",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="PREPROCESSING THE DATA",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = preprocess_data(train_request)
    current_step += 1

    ##### FEATURE ENGINEERING #####
    train_request = notify_java_server(train_request, new_status="FEATURE ENGINEERING THE DATA",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="FEATURE ENGINEERING THE DATA",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = feature_engineer_data(train_request)
    current_step += 1

    ##### ENCODING DATA #####
    train_request = notify_java_server(train_request, new_status="ENCODING THE DATA",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="ENCODING THE DATA",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = encode_data(train_request)
    current_step += 1

    ##### TRAINING MODEL #####
    train_request = notify_java_server(train_request, new_status="TRAINING THE MODEL",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="TRAINING THE MODEL",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = train_model(train_request)
    current_step += 1

    ##### SAVING MODEL #####
    train_request = notify_java_server(train_request, new_status="SAVING MODEL",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="SAVING MODEL",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    save_model(train_request)
    current_step += 1

    train_request = notify_java_server(train_request, new_status="TRAINING JOB FINISHED",
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state="TRAINING JOB FINISHED",
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})

    del train_request


def notify_java_server(train_request, new_status, progress):
    """
    Function that calls an endpoint from java server that updates the cached status of the train_request.
    :param train_request: train_request who's status wants to be updated
    :param new_status: new status of the train_request
    :return:
    """
    print(new_status, flush=True)
    train_request['state'] = new_status
    status_update = {'clientId': train_request['clientId'], 'requestId': train_request['requestId'],
                     'status': new_status, 'progress': progress}
    requests.post(Constants.BACKEND_UPDATE_REQUEST_STATUS, json=status_update)
    return train_request


# Mock Functions that describe the workflow
# TODO implement functions
def search_if_exists_already(train_request):
    pass


def persist_data(train_request):
    pass


def preprocess_data(train_request):
    flattened_json = pd.DataFrame(flatten(record) for record in json.loads(train_request["data"])["TrafficOccupancy"])
    print(flattened_json, flush=True)
    imputed_dataframe = fill_missing_values(dataframe=flattened_json,
                                            entity_id_columns=["ROAD_ID"],
                                            timestamp_id_columns=["TIMESTAMP"],
                                            numerical_fill=[('occupancy', 'interpolate')],
                                            categorical_fill=[]
                                            )
    output_json = imputed_dataframe.to_json(index=False, orient='table')
    train_request["data"] = output_json
    return train_request


def feature_engineer_data(train_request):
    return train_request


def encode_data(train_request):
    unencoded_data = pd.read_json(train_request["data"], orient='table')
    train_request['data'] = label_encode(unencoded_data).to_json(index=False, orient='table')
    return train_request


def train_model(train_request):
    full_data = pd.read_json(train_request['data'], orient='table')
    train_request['data'] = train_time_series_model(data=full_data,
                                                    algorithm="LGBM",
                                                    entity_columns=["ROAD_ID"],
                                                    timestamp_column=["TIMESTAMP"],
                                                    target=["occupancy"],
                                                    filepath="../saved_models/test.pkl"
                                                    )
    return train_request


def save_model(train_request):
    if not os.path.exists("saved_models/" + train_request["clientId"]):
        os.makedirs("saved_models/" + train_request["clientId"])
    current_time = time.strftime("%Y-%m-%d_%H%M%S")
    joblib.dump(train_request["data"], "saved_models/" + train_request["clientId"] + "/" +
                train_request["clientId"] + "_" + current_time + ".pkl")

    meta_info_job = {'filename': train_request["clientId"] + "_" + current_time + ".pkl",
                     'downloadlink': Constants.FLASK_ADDRESS + "/download-model/" + train_request["clientId"] + "_" + current_time + ".pkl",
                     'timestamp': current_time,
                     'clientid': train_request['clientId'],
                     'requestid': train_request['requestId'],
                     # 'metadata': train_request['metadata'],
                     }

    save_trained_model_to_db(meta_info_job)

    if os.path.exists('saved_models/meta_info.json'):
        with open('saved_models/meta_info.json') as f:
            data = json.load(f)
        data.append(meta_info_job)
        with open('saved_models/meta_info.json', 'w') as f:
            json.dump(data, f)
    else:
        with open('saved_models/meta_info.json', 'w') as f:
            json.dump([meta_info_job], f)

    pass
