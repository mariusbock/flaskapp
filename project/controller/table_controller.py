from project import db
from flask import make_response, jsonify, request, Response, render_template
import pandas as pd
from project.recipes.routes import recipes_blueprint
from project.repository.table_repository import *

class TableController:
    tableRepo = TableRepository()
    def save_to_db(self,data):
        return self.tableRepo.saveTableToDb(data)

    def get_data_from_db(self):
        return self.tableRepo.getDataFromDb()

    def insert_to_db(self,data):
        return self.tableRepo.insertValuesIntoTable(data)
