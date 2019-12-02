
from project.repository.table_repository import *
import pandas as pd

def test_save_table_into_db():

    tableRepo = TableRepository()
    jsonTable = {"type":"occupancy",
                 "fields": ["id", "occupancy", "vehicle_flow", "timestamp"]}
    data = pd.DataFrame(jsonTable)
    assert  tableRepo.saveTableToDb(data) == True

def test_insert_data_into_table():
    json = {"type":"occupancy",
            "values":["1","0.3","0.5","30.11.2019"]}
    data = pd.DataFrame(json)
    tableRepo = TableRepository()
    assert tableRepo.insertValuesIntoTable(data) == True


