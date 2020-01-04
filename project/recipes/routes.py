from project import db
from flask import make_response, jsonify, request, Response, render_template
from project.predictions import predict_occupancy
from project.models import TrainData
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import requests
from project.model.type_interrogation import *
from . import recipes_blueprint
from project.controller.protocol_cotroller import *
from project.controller.table_controller import *
from project.controller.request import Request,get_request_by_id
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
    REST Endpoint for testing connection between Java and Flask Server. The request from Java Server processed and
    compared with other data retrieved by the Flask Server
    :return: Ping successful or not conflict
    :raises: error message
    """

    def retrievePingMockData():
        """
        Function that calls and retrieves data from Java Server
        :return: returns response data as JSON
        """
        response = requests.get('http://127.0.0.1:8080/xtraffic-server/xtraffic-api/flaskresource/get-mock-data')
        print("Retrieved: ")
        print(response.json())
        return response.json()

    print("PING REQUEST FROM JAVA SERVER:\n")
    print(request.get_json())
    try:
        received_data = request.get_json()
        retrieved_data = retrievePingMockData()

        if received_data.get('teamname') == retrieved_data.get('teamname'):
            ok_response = {'message': 'true', 'code': 'SUCCESS'}
            print("PING REQUEST SUCCESFULL")
            return make_response(jsonify(ok_response), 200)

        else:
            bad_response = {'message': 'false', 'code': 'CONFLICT'}
            print("PING REQUEST UNSUCCESFULL")
            return make_response(jsonify(bad_response), 409)

    except Exception as e:
        print(e)


# def retrievePingMockData():
#     """
#     Function that calls and retrieves data from Java Server
#     :return: returns response data as JSON
#     """
#     response = requests.get('http://127.0.0.1:8080/xtraffic-server/xtraffic-api/flaskresource/get-mock-data')
#     print("Retrieved: ")
#     print(response.json())
#     return response.json()

@recipes_blueprint.route('/prediction-request', methods=['POST'])
def process_request():
    print("PROCESS REQUEST FROM JAVA SERVER:\n")
    request_json = request.get_json()
    request_id = request_json.get("requestId")
    client_id = request_json.get("clientId")
    data = request_json.get("data")
    meta_data = request_json.get("metadata")

    new_request = Request(request_id, client_id, data, meta_data)
    return make_response(jsonify(new_request.serialize()), 200)

@recipes_blueprint.route('/check-request-status/<request_id>', methods=['GET'])
def get_request_status(request_id):
    request_entity = get_request_by_id(request_id)
    mock_response = {}
    mock_response['requestId'] = request_id
    mock_response['clientId'] = "mock client id"
    mock_response['status'] = "mock status"

    response = {}
    response['requestId'] = request_entity.request_id
    response['clientId'] = request_entity.client_id
    response['status'] = request_entity.request_status

    json_data = json.dumps(response)



    return make_response(json_data, 200)
