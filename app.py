import flask
from flask import make_response, jsonify, request, json
from flask_restful import abort, Api
from predictions import predict_occupancy

# Initialize the app
app = flask.Flask(__name__)
api = Api(app)




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


@app.route('/predictOccupancy', methods = ['POST'])
def api_predict_occupancy():
    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        processed_data = predict_occupancy(data)

        print(processed_data)

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


if __name__ == '__main__':
    app.run()