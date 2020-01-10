from project.celery import celery
from project.predictions import preprocess_dataset
from project.controller import request
import random
import time

@celery.task
def preprocess_wrapper(df):
    preprocess_dataset(df)

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