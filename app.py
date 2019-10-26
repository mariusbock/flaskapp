import flask
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import time
from flask import make_response, jsonify, request, json
from flask_restful import abort, Api
from predictions import predict_occupancy
import requests

# Initialize the app
app = flask.Flask(__name__)
api = Api(app)


def update_models():
    """ Function for test purposes. """
    """ Here would the call of the Backend API happen, needs to be implemented with Victor"""
    print("If this would work it would update models!")


"""
POST method predictOccupancy that returns the predicted occupancy using the latest trained model for the given parsed_data. 
Needs to have a JSON attached in the body following the needed format.

Returns:
    Returns a JSON file containing the predicted occupancy for the given parsed_data

Raises:
    415 Unsupported Media Type if it is not a JSON in the body
"""
@app.route('/predictOccupancy', methods = ['POST'])
def api_predict_occupancy():
    if request.headers['Content-Type'] == 'application/json':

        data = request.json
        # TODO: Exception Handling of when JSON does not follow correct format
        processed_data = predict_occupancy(data)

        resp = jsonify(processed_data)

        resp.status_code = 200

        return resp
    else:
        return "415 Unsupported Media Type"


@app.route('/')
def api_root():
    return 'Welcome'


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"




@app.route('/flask-ping-endpoint', methods = ['POST'])
def processPing():
    """REST Endpoint for testing connection between Java and Flask Server"""
    """the request from Java Server processed and compared with other data retrieved by the Flask Server """
    print("PING REQUEST FROM JAVA SERVER:\n")
    print(request.get_json())
    try:
        received_data = request.get_json()
        retrieved_data = retrievePingMockData()

        if received_data.get('teamname') == retrieved_data.get('teamname'):
            ok_response = {'message':'true', 'code': 'SUCCESS'}
            print("PING REQUEST SUCCESFULL")
            return make_response(jsonify(ok_response), 200)

        else:
            bad_response = {'message':'false', 'code': 'CONFLICT'}
            print("PING REQUEST UNSUCCESFULL")
            return make_response(jsonify(bad_response), 409)

    except Exception as e:
        print(e)

def retrievePingMockData():
    """Function that calls and retrieves data from Java Server"""
    response = requests.get('http://localhost:8080/xtraffic-server/xtraffic-api/flaskresource/get-mock-data')
    print("Retrieved: ")
    print(response.json())
    return response.json()




sched = BackgroundScheduler(daemon=True)
sched.add_job(update_models,'interval', seconds=10)
sched.start()


if __name__ == '__main__':
    app.run()
