"""
This file (test_protocol.py) contains all unit tests for the protocol_repository.py file
"""
from project.model.type_interrogation import *
from project.repository.protocol_repository import *


def test_check_missing_data():
    typeInterogation = TypeInterrogation("occupancy", ["id", "occupancy", "vehicle_flow", "timestamp"], {})
    flasRequest = ("1", typeInterogation, {"treshold": "0.05",
                                           "timestamp": "30.11.2019",
                                           "records": "1"})
    protocol = Protocol(flasRequest)
    protocolRepo = ProtocolRepository(protocol)
    assert protocolRepo.check_missing_data() == True
