import json
import os
import requests
from flask import url_for, render_template, request, jsonify, make_response, send_file

from config import Constants
from project.celery import celery_wrappers, celery
from project.recipes import recipes_blueprint


@recipes_blueprint.route('/')
def index():
    return render_template("recipes/index.html")


@recipes_blueprint.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@recipes_blueprint.route('/flask-ping-endpoint', methods=['POST'])
def processPing():
    """
    REST Endpoint for testing connection between Java and Flask Server. The train_request from Java Server processed and
    compared with other data retrieved by the Flask Server
    :return: Ping successful or not conflict
    :raises: error message
    """

    def retrievePingMockData():
        """
        Function that calls and retrieves data from Java Server
        :return: returns response data as JSON
        """
        response = requests.get(Constants.BACKEND_GET_MOCK_DATA)
        print("Retrieved: ")
        print(response.json())
        return response.json()

    print("PING REQUEST FROM JAVA SERVER:\n")
    print(request.get_json())
    try:
        received_data = request.get_json()
        retrieved_data = retrievePingMockData()

        if received_data.get('teamname') == retrieved_data.get('teamname'):
            ok_response = {'message': 'true',
                           'code': 'SUCCESS',
                           'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Credentials': '*',
                           'Access-Control-Allow-Headers': '*',
                           'Access-Control-Allow-Methods': '*'}
            print("PING REQUEST SUCCESFULL")
            return make_response(jsonify(ok_response), 200)

        else:
            bad_response = {'message': 'false',
                            'code': 'CONFLICT',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Credentials': '*',
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Methods': '*'}
            print("PING REQUEST UNSUCCESFULL")
            return make_response(jsonify(bad_response), 409)

    except Exception as e:
        print(e)


@recipes_blueprint.route('/download-model/<filename>', methods=['GET'])
def download_model(filename):
    client_id = filename.split("_")[0]
    return send_file(os.path.join(os.getcwd(),'saved_models/' + client_id + "/" + filename), as_attachment=True)


@recipes_blueprint.route('/train-request', methods=['POST'])
def process_train_request():
    print("PROCESS TRAIN REQUEST FROM JAVA SERVER:\n")
    request_json = request.get_json()
    celery_wrappers.process_train_request(request_json)

    return make_response("Model Successfully Trained", 200)


@recipes_blueprint.route('/check-request-status/<request_id>', methods=['GET'])
def get_request_status(request_id):
    request_entity = celery.AsyncResult(request_id)

    response = {'clientId': request_entity.info["client_id"],
                'requestId': request_entity.info["request_id"],
                'status': request_entity.state,
                'progress': request_entity.info["progress"]}
    json_data = json.dumps(response)

    return make_response(json_data, 200)


@recipes_blueprint.route('/get-all-trained-models', methods=['GET'])
def get_all_trained_models():
    if os.path.exists('saved_models/meta_info.json'):
        with open('saved_models/meta_info.json') as f:
            response = json.load(f)
    else:
        response = {}
    json_data = json.dumps(response)

    return make_response(json_data, 200)


@recipes_blueprint.route('/test-celery', methods=['GET'])
def test_celery():
    response = {}
    response['status'] = celery_wrappers.test_bg_job()
    json_response = json.dumps(response)
    return make_response(json_response, 200)


@recipes_blueprint.route('/test-celery-complex', methods=['GET'])
def longtask():
    print("TEST CELERY COMPLEX")
    task = celery_wrappers.test_complex_bg_job.apply_async(thread=False)
    return jsonify({'taskid': task.id}), 202, {'Location': url_for('recipes.taskstatus',
                                                                   task_id=task.id)}


@recipes_blueprint.route('/status/<task_id>')
def taskstatus(task_id):
    task = celery_wrappers.test_complex_bg_job.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
