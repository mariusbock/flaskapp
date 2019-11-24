"""
This file (test_protocol.py) contains all unit tests for the protocol.py file
"""
from project.protocol import *
def test_grab_missing_data():

    listOfIterogations = []
    typeInterrogation = {"type":"status","fields": ["id", "datetime", "occupancy", "vehicle_flow","timestamp"], "rule": ""}
    listOfIterogations.append(typeInterrogation)
    requestFromServer = {"requestId": 1,"listOfInterogations": listOfIterogations,"matchingRule": {}}
    assert Protocol(requestFromServer).grab_missing_data == True
