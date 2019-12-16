from flask import make_response, jsonify
from sqlalchemy import inspect
from project import db
from pandas import DataFrame
from project.model.protocol import *
from project.repository.table_repository import *
class ProtocolRepository:

    tableRepo = TableRepository()
    def check_missing_data(self):
        with open('static/test_data/protocol_request.json') as fh:
            mystr = fh.read()
        val = json.loads(mystr)
        treshold = val['matchingRule']['treshold']
        timestamp = val['matchingRule']['timestamp']
        amountOfRecords =val['matchingRule']['records']
        for interrogation in val['typeInterrogations']:
            table_name = interrogation['type']
            numberOfEntriesForGivenTimestamp = self.tableRepo.count_entries_in_table(timestamp)
            x = numberOfEntriesForGivenTimestamp/amountOfRecords
            # ins = inspect(db.engine)
            # for _t in ins.get_table_names():
            #     if _t == table_name:
            #         if _t.columns.size != interrogation['fields'].size:
            #             raise ("Tables are not of equal number of columns")
            if x < treshold:
                self.tableRepo.delete_old_entries_from_table(interrogation['fields'])
                raise("Number of entries above threshold. All entries from given table already deleted!")
            else :
                return True
        return False

    def send_response_to_server(self):
        result = self.check_missing_data()
        if result == True:
            ok_response = {'message': 'true', 'code': 'SUCCESS'}
            print("ALL DATA IS AVAILABLE")
            return make_response(jsonify(ok_response), 200)
        else:
            bad_response = {'message': 'false', 'code': 'CONFLICT'}
            print("DATA IS MISSING")
            # TODO call functions from state.py that refreshes tables and persists data

            return make_response(jsonify(bad_response), 409)

    def get_response_from_xData(self, table_name):
        # TODO get real number of entries from xdata server for a specific table instead of mockresponse
        # return State(table_name).count_entries_in_table()
        return 1