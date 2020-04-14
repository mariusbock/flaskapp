import pytest

from project import create_app, local_db
from project.local_db.models import TrainData

"""
File that contains all fixtures used for testing the application. They can be used in all tests.
"""


@pytest.fixture(scope='module')
def new_traindata():
    """
    Creates new training record
    :return: sample training record
    """
    trainrecord = {"timestamp": "2019-10-14 13:32:00+00:00",
                   "id": "18371007[D40a]",
                   "last_occupancy": 16.5, "last_1_occupancy": 6.6667, "last_5_occupancy": 14.5,
                   "occupancy": 15.5}

    print(trainrecord)
    return trainrecord


@pytest.fixture(scope='module')
def test_client():
    """
    Creates new instance of app and test client.
    :return: test result
    """
    flask_app = create_app('config.py')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    """
    Create instance of database and add two records.
    :return: test result
    """
    # Create the database and the database table
    local_db.create_all()

    # Insert user data
    train_record1 = TrainData('2019-09-14 13:32:00+00:00', 'TEST_ID', 1.13, 6.66667, 14.5, 15.5)
    train_record2 = TrainData('2019-09-12 13:32:00+00:00', 'ANOTHER_TEST_ID', 1634656.3, 6.66667, 14.5, 15.5)
    local_db.session.add(train_record1)
    local_db.session.add(train_record2)

    # Commit the changes for the users
    local_db.session.commit()

    yield local_db  # this is where the testing happens!

    local_db.drop_all()
