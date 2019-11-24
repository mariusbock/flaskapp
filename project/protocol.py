from flask import make_response, jsonify
from sqlalchemy import inspect
from project import db
from project.state import State
import pandas as pd
from pandas import DataFrame
from project.status import Status

class Protocol():


    requestFromServer = {}
    requestId = 0
    interrogationsList = []
    matchingRule = {}

    def __init__(self, requestFromServer):
        status = Status("1", "23.11.2019", "0.4", "0.4")
        data = {"id": [status.id], "timestamp": [status.timestamp], "occupancy": [status.occupancy], "vehicle_flow": [status.vehicle_flow]}
        df = DataFrame(data)
        df.to_sql('Status', con=db.engine, index=False, if_exists="replace")

        self.requestFromServer = requestFromServer
        self.requestId = self.requestFromServer['requestId']
        self.interrogationsList = self.requestFromServer['listOfInterogations']
        self.matchingRule = self.requestFromServer['matchingRule']

    def grab_missing_data(self):
        # each interogation contains a table_name and a list of table columns
        for interogation in self.interrogationsList:
            table_name = getattr(interogation,'type')
            entriesFromServer = self.get_response_from_xData(table_name)
            # check table names exists via inspect
            ins = inspect(db.engine)
            for _t in ins.get_table_names():
                if _t == table_name:
                    entriesFromDb = State(_t).count_entries_in_table()
                    i = 0
                    #if number of columns from db not equal with number of tables from request
                    if _t.columns.size != interogation['fields'].size:
                        return False
                    else:
                        #if column names from db not equal to column names from server request
                        for columnsFromDb in _t.columns:
                            if columnsFromDb != interogation['fields'][i]:
                                return False
                            i = i + 1
                    #if the number of entries from db not equal to number of entries from request
                    if entriesFromDb != entriesFromServer:
                        return False
                    return True

        return False

    def send_response_to_server(self):
        result = self.grab_missing_data
        if result == True:
            ok_response = {'message': 'true', 'code': 'SUCCESS'}
            print("ALL DATA IS AVAILABLE")
            return make_response(jsonify(ok_response), 200)
        else:
            bad_response = {'message': 'false', 'code': 'CONFLICT'}
            print("DATA IS MISSING")
            return make_response(jsonify(bad_response), 409)

    def get_response_from_xData(self,table_name):
        #TODO get real number of entries from xdata server for a specific table instead of mockresponse
        #return State(table_name).count_entries_in_table()
        return 1

# def main():
#     listOfIterogations = []
#     typeInterrogation = {"type": "status", "fields": ["id", "datetime", "occupancy", "vehicle_flow", "timestamp"],
#                          "rule": ""}
#     listOfIterogations.append(typeInterrogation)
#     requestFromServer = {"requestId": 1, "listOfInterogations": listOfIterogations, "matchingRule": {}}
#     protocol1 = Protocol(requestFromServer)
#     protocol1.grab_missing_data()
#
#
# if __name__ == '__main__':
#     main()