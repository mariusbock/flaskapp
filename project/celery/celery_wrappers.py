import requests

from project.celery import celery
from project.predictions import preprocess_dataset
from project.controller import request
import random
import time



@celery.task
def test_bg_job():
    print("THIS STRING WAS PRINTED FROM A BACKGROUND JOB")
    return "Simple Background Job test Succesful. Look on the server log to see if a message was printed"

@celery.task(bind=True,track_started=True)
def test_complex_bg_job(self):
    print("INITIATED BG JOB...\n")
    status_int = 0
    status = "INITIALIZED"
    for i in range(10):
        print("NEW ITERATION...\n")
        if (status_int<2):
            status = "INITIALIZED"

        elif (status_int >= 2 or status_int < 6 ):
            status = "PREPROCESSING"

        elif (status_int >= 6 or status_int <= 9):
            status = "COMPUTATING"

        else:
            status = "FINISHED"

        self.update_state(state=status, meta={'current': status_int, 'status': status_int})
        time.sleep(5)
        status_int += 1

    return {'current': 100, 'status': 'Task completed!', 'result': 42}

@celery.task(bind=True,track_started=True)
def process_request(self, Request):
    current_step = 0
    total_steps = 6    #the number of suboperations in a task, used for displaying a progress in percent -> more steps = change this int!

    current_step+=1
    self.update_state(state="SEARCHING FOR REQUEST", meta={'request_id':Request.request_id, 'client_id': Request.client_id, 'progress':(current_step/total_steps)*100})
    search_if_exists_already(Request)
    notify_java_server(Request, newStatus="SEARCHING FOR REQUEST")

    current_step+=1
    self.update_state(state="PERSISTING THE DATA", meta={'request_id':Request.request_id, 'client_id': Request.client_id, 'progress':(current_step/total_steps)*100})
    persist_data(Request)
    notify_java_server(Request, newStatus="PERSISTING THE DATA")

    current_step+=1
    self.update_state(state="PREPROCESSING THE DATA", meta={'request_id':Request.request_id, 'client_id': Request.client_id, 'progress':(current_step/total_steps)*100})
    preprocess_data(Request)
    notify_java_server(Request, newStatus="PREPROCESSING THE DATA")

    current_step+=1
    self.update_state(state="TRAINING THE MODEL", meta={'request_id':Request.request_id, 'client_id': Request.client_id, 'progress':(current_step/total_steps)*100})
    train_model(Request)
    notify_java_server(Request, newStatus="TRAINING THE MODEL")

    current_step+=1
    self.update_state(state="PERSISTING THE RESULT", meta={'request_id':Request.request_id, 'client_id': Request.client_id, 'progress':(current_step/total_steps)*100})
    persist_result(Request)
    notify_java_server(Request, newStatus="PERSISTING THE RESULT")


def notify_java_server(Request, newStatus):
    #function that calls an endpoint from java server that updates the cached status
    pass


#Mock Functions that describe the workflow
#TODO implement functions
def search_if_exists_already(Request):
    pass

def persist_data(Request):
    pass

def preprocess_data(Request):
    pass

def train_model(Request):
    pass

def predict_occupancy(Request):
    pass

def persist_result(Request):
    pass
