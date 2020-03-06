from project.predictions import predict_occupancy
from project.models import TrainData
from project.controller.protocol_cotroller import *
from project.controller.table_controller import *
from project.celery import celery_wrappers

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
    data = pd.read_sql(sql=db.session.query(TrainData)
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

@recipes_blueprint.route('/grab-missing-data', methods=['POST'])
def grab_missing_data():
    print("PROCESS REQUEST FROM JAVA SERVER:\n")
    protocolController = ProtocolController()
    return protocolController.grab_missing_data()

@recipes_blueprint.route('/save-table', methods=['POST'])
def save_table_to_db():
    data = pd.DataFrame({"type":[request.json]})
    tableController = TableController()
    if request.headers['Content-Type'] == 'application/json':
        tableController.save_to_db(data)
        return "Table saved into the Db."
    else:
        return "415 Unsupported Media Type"

@recipes_blueprint.route('/get-table', methods=['GET'])
def get_table_from_db():
    tableController = TableController()
    return tableController.get_data_from_db()

@recipes_blueprint.route('/insert-values', methods=['POST'])
def insert_into_table():
    data = pd.DataFrame(request.json)
    tableController = TableController()
    if request.headers['Content-Type'] == 'application/json':
        tableController.insert_to_db(data)
        return "Values inserted into the table."
    else:
        return "415 Unsupported Media Type"

@recipes_blueprint.route('/test-celery', methods=['GET'])
def test_celery():
    celery_wrappers.test_bg_job()

# @recipes_blueprint.route('/grab-missing-data', methods=['POST'])
# def grab_missing_data():
#     print("PROCESS REQUEST FROM JAVA SERVER:\n")tes
#     print(request.get_json())
#
#     response = request.get_json()
#     protocol = Protocol(response)
#     return protocol.send_response_to_server()
