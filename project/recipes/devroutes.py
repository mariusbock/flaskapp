from flask import request, make_response, jsonify
import requests

from config import Constants
from project.celery import celery_wrappers
from project.recipes import recipes_blueprint


@recipes_blueprint.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    """
    Echo function to test different methods with Flask server
    :return: echo response
    """
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@recipes_blueprint.route('/test-celery', methods=['GET'])
def test_celery():
    """
    Route to test celery functionality. Starts a sample job that goes through different stages.
    :return: response
    """
    celery_wrappers.test_bg_job()


@recipes_blueprint.route('/flask-ping-endpoint', methods=['POST'])
def process_ping():
    """
    REST Endpoint for testing connection between Java and Flask Server. The train_request from Java Server processed and
    compared with other data retrieved by the Flask Server
    :return: Ping successful or not conflict
    :raises: error message
    """

    def retrieve_ping_mock_data():
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
        retrieved_data = retrieve_ping_mock_data()

        if received_data.get('teamname') == retrieved_data.get('teamname'):
            ok_response = {'message': 'true',
                           'code': 'SUCCESS'}
            print("PING REQUEST SUCCESSFUL")
            return make_response(jsonify(ok_response), 200)

        else:
            bad_response = {'message': 'false',
                            'code': 'CONFLICT'}
            print("PING REQUEST UNSUCCESSFUL")
            return make_response(jsonify(bad_response), 409)

    except Exception as e:
        print(e)

