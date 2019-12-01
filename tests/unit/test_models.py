"""
This file (test_models.py) contains all unit tests for the models.py file
"""
from project.protocol import Protocol

def test_new_traindata(new_traindata):
    """
    GIVEN a Traindata model
    WHEN a new trainrecord is created
    THEN check the timestamp, id, last_occupancy, last_1_occupancy, last_5_occupancy and occupancy fields are defined correctly
    """
    print(new_traindata)
    assert new_traindata.timestamp == "2019-10-14 13:32:00+00:00"
    assert new_traindata.id == "18371007[D40a]"
    assert new_traindata.last_occupancy == 16.5
    assert new_traindata.last_1_occupancy == 6.6667
    assert new_traindata.last_5_occupancy == 14.5
    assert new_traindata.occupancy == 15.5


