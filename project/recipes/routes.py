
import requests
from project.controller.table_controller import *
from project.controller.request import Request, get_request_by_id
from project.celery import celery_wrappers
from project.recipes import recipes_blueprint
from flask import url_for


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
        response = requests.get('http://backend:8080/xtraffic-server/xtraffic-api/flaskresource/get-mock-data')
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
                           'Access-Control-Allow-Headers':'*',
                           'Access-Control-Allow-Methods':'*'}
            print("PING REQUEST SUCCESFULL")
            return make_response(jsonify(ok_response), 200)

        else:
            bad_response = {'message': 'false',
                            'code': 'CONFLICT',
                            'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Credentials': '*',
                           'Access-Control-Allow-Headers':'*',
                           'Access-Control-Allow-Methods':'*'}
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
    return jsonify({'taskid':task.id}), 202, {'Location': url_for('recipes.taskstatus',
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