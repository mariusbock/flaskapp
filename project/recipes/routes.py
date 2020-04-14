import json
import os
from flask import render_template, request, jsonify, make_response, send_file

from project.celery import celery_wrappers, celery
from project.recipes import recipes_blueprint


@recipes_blueprint.route('/')
def index():
    """
    Index page route seen by user if he accesses the website of Flask
    :return index page
    """
    return render_template("recipes/index.html")


@recipes_blueprint.errorhandler(404)
def not_found():
    """
    404 not found page
    :return 404 not found response
    """
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@recipes_blueprint.route('/download-model/<filename>', methods=['GET'])
def download_model(filename):
    """
    Route to download model from Flask
    :param filename: filename that wants to be accessed and downloaded
    :return: model file
    """
    client_id = filename.split("_")[0]
    return send_file(os.path.join('/flask-app/project/saved_models/' + client_id + "/" + filename), as_attachment=True)


@recipes_blueprint.route('/train-request', methods=['POST'])
def process_train_request():
    """
    Route used to train model. Request needs to contain all needed information.
    :return: alert that model trained successfully (NOTE: should be optimised)
    """
    print("PROCESS TRAIN REQUEST FROM JAVA SERVER:\n")
    # Get JSON element of request
    request_json = request.get_json()
    print(request_json)
    # Pass JSON to celery wrapper function
    celery_wrappers.process_train_request(request_json)

    return make_response("Model Successfully Trained", 200)


@recipes_blueprint.route('/check-request-status/<request_id>', methods=['GET'])
def get_request_status(request_id):
    """
    Route to get the status of a train or prediction request
    :param request_id: id of the request that status is wanted from
    """
    # Get Celery entity of request
    request_entity = celery.AsyncResult(request_id)

    # Create response item containing all wanted information
    response = {'clientId': request_entity.info["client_id"],
                'requestId': request_entity.info["request_id"],
                'status': request_entity.state,
                'progress': request_entity.info["progress"]}
    json_data = json.dumps(response)

    return make_response(json_data, 200)


@recipes_blueprint.route('/get-all-trained-models', methods=['GET'])
def get_all_trained_models():
    """
    Route to receive a list of all trained models saved on Flask.
    :return: JSON of all saved models
    """
    # Check if meta_info.json file exists, if not return empty JSON
    if os.path.exists('saved_models/meta_info.json'):
        with open('saved_models/meta_info.json') as f:
            response = json.load(f)
    else:
        response = {}

    json_data = json.dumps(response)

    return make_response(json_data, 200)

