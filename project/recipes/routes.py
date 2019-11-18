from project import db
from flask import make_response, jsonify, request, Response, render_template
from project.predictions import predict_occupancy
from project.models import TrainData
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import requests

from . import recipes_blueprint


@recipes_blueprint.route('/')
def index():
    return render_template("recipes/index.html")


@recipes_blueprint.route('/predictOccupancy', methods=['POST'])
def api_predict_occupancy():
    """
    POST method predictOccupancy that returns the predicted occupancy using the latest trained model for the given
    parsed_data. Needs to have a JSON attached in the body following the needed format.
    :return: Returns a JSON file containing the predicted occupancy for the given parsed_data
    :raises: 415 Unsupported Media Type if it is not a JSON in the body
    """
    if request.headers['Content-Type'] == 'application/json':

        data = pd.DataFrame(request.json)
        print(data)
        # TODO: Exception Handling of when JSON does not follow correct format
        processed_data = predict_occupancy(data)

        resp = jsonify(processed_data)

        resp.status_code = 200

        return resp
    else:
        return "415 Unsupported Media Type"


@recipes_blueprint.route('/saveToDB', methods=['POST'])
def save_to_db():
    if request.headers['Content-Type'] == 'application/json':

        data = pd.DataFrame(request.json)
        print(data)

        data.to_sql('TrainData', con=db.engine, index=False, if_exists="replace")

        return "All train data saved to DB."
    else:
        return "415 Unsupported Media Type"


@recipes_blueprint.route('/getDataFromDB', methods=['GET'])
def get_data_from_db():
    data = pd.read_sql(sql=db.session.query(TrainData) \
                       .with_entities(TrainData.timestamp,
                                      TrainData.id,
                                      TrainData.last_occupancy,
                                      TrainData.last_1_occupancy,
                                      TrainData.last_5_occupancy,
                                      TrainData.occupancy).statement,
                       con=db.session.bind)

    resp = Response(response=data.to_json(orient='records'),
                    status=200,
                    mimetype="application/json")

    return resp


@recipes_blueprint.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@recipes_blueprint.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
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


@recipes_blueprint.route('/flask-ping-endpoint', methods=['POST'])
def processPing():
    """
    REST Endpoint for testing connection between Java and Flask Server. The request from Java Server processed and
    compared with other data retrieved by the Flask Server
    :return: Ping successful or not conflict
    :raises: error message
    """
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


def retrievePingMockData():
    """
    Function that calls and retrieves data from Java Server
    :return: returns response data as JSON
    """
    response = requests.get('http://localhost:8080/xtraffic-server/xtraffic-api/flaskresource/get-mock-data')
    print("Retrieved: ")
    print(response.json())
    return response.json()


def update_models():
    """ Function for test purposes. """
    """ Here would the call of the Backend API happen, needs to be implemented with Victor"""
    print("If this would work it would update models!")


"""
Following code is the scheduler that executes the update model function periodically. Currently only skeleton with no
function.
"""
sched = BackgroundScheduler(daemon=True)
sched.add_job(update_models, 'interval', seconds=10)
sched.start()
