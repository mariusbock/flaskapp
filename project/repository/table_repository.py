import json

import numpy
import pandas as pd
from flask import Response
from sqlalchemy.types import Integer, DateTime

from project.model.status import *


# class which contains all relevant info(functions and data) regarding tables
class TableRepository:

    def saveTableToDb(self, data):
        try:
            table_name = data['type']
            if table_name[0]['type'] == "status":
                with open('static/test_data/status_columns.json') as fh:
                    mystr = fh.read()
                val = json.loads(mystr)
                status_df = pd.DataFrame.from_dict(val, orient="columns")
                print(status_df)
                status_df.to_sql("status", con=db.engine, index=False, if_exists="replace")
                return True
            else:
                return False
        except:
            raise ValueError("Table could not be saved")

    def insertValuesIntoTable(self, data):
        try:
            table_name = data['type']
            if table_name[0] == "status":
                val = numpy.array(data['values'][0])
                print(val)
                status_df = pd.DataFrame.from_dict(val, orient="columns")
                status = Status(data['values'][0]['id'], data['values'][0]['timestamp'],
                                data['values'][0]['occupancy'], data['values'][0]['vehicle_flow'])
                print(status_df)
                status_df.to_sql("status", con=db.engine, index=False, if_exists="append",
                                 dtype={"id": Integer, "occupancy": float, "vehicle_flow": float,
                                        "timestamp": DateTime})
                return True
        except:
            raise ValueError("Values could not be inserted")

    def getDataFromDb(self):
        try:
            query = "SELECT * FROM status"
            data_df = pd.read_sql_query(query, db.engine)
            resp = Response(response=data_df.to_json(orient='records'),
                            status=200,
                            mimetype="application/json")
            return resp
        except:
            raise ValueError("Info could not be taken from table")

    # count entries from table occupacy for a specific timestamp
    def count_entries_in_table(self, timestamp):
        try:
            script = "select count(id) from status where timpestamp %(time)s "
            count = db.engine.execute(script, params={"time": timestamp}, index_col=['timestamp']).fetchAll()
            return count.scalar()
        except:
            raise ValueError("Error by counting entries from table")

    def delete_old_entries_from_table(self, fields):
        try:
            to_drop_columns = fields
            df = pd.drop(columns=to_drop_columns, inplace=True)
            return df
        except:
            raise ValueError("Error by deleting old entries from table")

    def add_new_entries_to_table(self):
        # TODO function which insert new entries from xdata
        return 0
