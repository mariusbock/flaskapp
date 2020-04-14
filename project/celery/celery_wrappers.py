import json
import os
import time
from datetime import datetime

import pandas as pd
import requests
from flatten_json import flatten
from sklearn.externals import joblib

from config import Constants
from project.celery import celery
from project.machine_learning.feature_engineering import create_your_own_feature
from project.machine_learning.model_training import train_time_series_model
from project.machine_learning.preprocessing import fill_missing_values, label_encode
from project.training_db.training_db_cotroller import save_trained_model_to_db, save_created_feature_to_db

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
    print('THIS STRING WAS PRINTED FROM A BACKGROUND JOB')
    return 'Simple Background Job test Successful. Look on the server log to see if a message was printed'


@celery.task(bind=True, track_started=True)
def test_complex_bg_job(self):
    """
    Sample complex background task with multiple stages.
    :return: Status message
    """
    print('INITIATED BG JOB...\n')
    status_int = 0
    for i in range(10):
        print('NEW ITERATION...\n')
        if status_int < 2:
            status = 'INITIALIZED'

        elif status_int >= 2 or status_int < 6:
            status = 'PREPROCESSING'

        elif status_int >= 6 or status_int <= 9:
            status = 'COMPUTATING'

        else:
            status = 'FINISHED'

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
    # TODO Better error handling
    current_step = 0
    # number of suboperations in a task, used for displaying a progress in percent -> more steps = change this int!
    total_steps = 5

    ##### TRAINING STARTED #####
    train_request = notify_java_server(train_request, new_status='TRAINING JOB STARTED',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='TRAINING JOB STARTED',
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})

    ##### PREPROCESSING #####
    train_request = notify_java_server(train_request, new_status='PREPROCESSING THE DATA',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='PREPROCESSING THE DATA',
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = preprocess_data(train_request)
    current_step += 1

    ##### FEATURE ENGINEERING #####
    train_request = notify_java_server(train_request, new_status='FEATURE ENGINEERING THE DATA',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='FEATURE ENGINEERING THE DATA',
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = feature_engineer_data(train_request)
    current_step += 1

    ##### ENCODING DATA #####
    train_request = notify_java_server(train_request, new_status='ENCODING THE DATA',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='ENCODING THE DATA',
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = encode_data(train_request)
    current_step += 1

    ##### TRAINING MODEL #####
    train_request = notify_java_server(train_request, new_status='TRAINING THE MODEL',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='TRAINING THE MODEL',
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    train_request = train_model(train_request)
    current_step += 1

    ##### SAVING MODEL #####
    train_request = notify_java_server(train_request, new_status='SAVING MODEL',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='SAVING MODEL',
                      meta={'request_id': train_request['requestId'], 'client_id': train_request['clientId'],
                            'progress': (current_step / total_steps) * 100})
    save_model(train_request)
    current_step += 1

    ##### TRAINING FINISHED #####
    train_request = notify_java_server(train_request, new_status='TRAINING JOB FINISHED',
                                       progress=(current_step / total_steps) * 100)
    self.update_state(task_id=train_request['requestId'],
                      state='TRAINING JOB FINISHED',
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


def preprocess_data(train_request):
    """
    Function that applies wanted preprocessing defined in request on top of data contained in request
    :param train_request: train request that contains information
    :return: train request with preprocessed data
    """
    # TODO have preprocessing information extracted from train request
    flattened_json = pd.DataFrame(flatten(record) for record in json.loads(train_request['data'])['TrafficOccupancy'])
    print(flattened_json, flush=True)
    # Currently only does filling of missing values
    imputed_dataframe = fill_missing_values(dataframe=flattened_json,
                                            entity_id_columns=['ROAD_ID'],
                                            timestamp_id_columns=['TIMESTAMP'],
                                            numerical_fill=[('occupancy', 'interpolate')],
                                            categorical_fill=[]
                                            )
    output_json = imputed_dataframe.to_json(index=False, orient='table')
    train_request['data'] = output_json
    return train_request


def feature_engineer_data(train_request):
    # read training info object that contains all meta infos about training process
    training_info = train_request['trainingInfo']
    training_data = pd.read_json(train_request['data'], orient='table')
    engineered_features = pd.DataFrame()

    for created_feature in training_info['createdFeatures']:
        current_time = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
        # created feature record that is saved to training database
        created_feature_record = {
            'id': created_feature['featureName'] + '_' + train_request['clientId'] + '_' + current_time,
            'name': created_feature['featureName'],
            'description': created_feature['featureDescription'],
            'timestamp': current_time,
            'clientid': train_request['clientId'],
            'requestid': train_request['requestId'],
            'sqlstatement': created_feature['sqlStatement']
        }

        # check if SQL statement has any effect
        if not create_your_own_feature(created_feature['sqlStatement'], training_data).empty:
            # if does, check if result dataframe is empty, if so initialize result dataframe
            if engineered_features.empty:
                engineered_features = create_your_own_feature(created_feature['sqlStatement'], training_data)
            # if not append to result dataframe
            else:
                engineered_features = pd.concat(engineered_features,
                                                create_your_own_feature(created_feature['sqlStatement'], training_data))
            # save database record to training database
            save_created_feature_to_db(created_feature_record)

    print('ENGINEERED FEATURES:', flush=True)
    print(engineered_features, flush=True)
    # append engineered features to training dataframe
    train_request['data'] = pd.concat([training_data, engineered_features]).to_json(index=False, orient='table')
    return train_request


def encode_data(train_request):
    """
    Function that label encodes the data according to wanted label encoding of user
    :param train_request: train request to be handeled
    :return: label-encoded train request
    """
    # TODO make this more modular
    unencoded_data = pd.read_json(train_request["data"], orient='table')
    train_request['data'] = label_encode(unencoded_data).to_json(index=False, orient='table')
    return train_request


def train_model(train_request):
    """
    Function that trains model according to user defined model selection
    :param train_request: train request to be used for training
    :return: train_request element with trained model as data parameter
    """
    full_data = pd.read_json(train_request['data'], orient='table')
    train_request['data'] = train_time_series_model(data=full_data,
                                                    algorithm='LGBM',
                                                    timestamp_column=['TIMESTAMP'],
                                                    target=['occupancy'],
                                                    )
    return train_request


def save_model(train_request):
    """
    Function that saves model locally and saves meta information to training database and local json file
    :param train_request: train_request to be used
    """
    # read training info object that contains all meta infos about how to save model
    training_info = train_request['trainingInfo']

    # check if saved_models folder exists
    if not os.path.exists('/flask-app/project/saved_models/' + train_request['clientId']):
        os.makedirs('/flask-app/project/saved_models/' + train_request['clientId'])
    current_time = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]

    # save model as pickle file and store in saved_models folder on Flask server
    joblib.dump(train_request['data'], '/flask-app/project/saved_models/' + train_request['clientId'] + '/' +
                train_request['clientId'] + '_' + current_time + '.pkl')

    # trained model record to be saved in database
    trained_model_record = {'id': train_request['clientId'] + "_" + current_time,
                            'name': training_info['modelMeta']['modelName'],
                            'description': training_info['modelMeta']['modelDescription'],
                            'timestamp': current_time,
                            'clientid': train_request['clientId'],
                            'requestid': train_request['requestId'],
                            'downloadlink': Constants.FLASK_ADDRESS + '/download-model/' + train_request[
                                'clientId'] + "_" + current_time + '.pkl',
                            }

    # save trained model record to training database
    save_trained_model_to_db(trained_model_record)

    # save meta infos locally, that would breack relational schema (extended information
    if os.path.exists('/flask-app/project/saved_models/meta_info.json'):
        with open('/flask-app/project/saved_models/meta_info.json') as f:
            data = json.load(f)
        data.append(trained_model_record)
        with open('/flask-app/project/saved_models/meta_info.json', 'w') as f:
            json.dump(data, f)
    else:
        with open('/flask-app/project/saved_models/meta_info.json', 'w') as f:
            json.dump([trained_model_record], f)

    pass
