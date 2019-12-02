import pytest
import pandas as pd
from project import create_app, db
from project.models import TrainData


@pytest.fixture(scope='module')
def new_traindata():
    trainrecord = TrainData(timestamp="2019-10-14 13:32:00+00:00", id="18371007[D40a]", last_occupancy=16.5,
                            last_1_occupancy=6.6667, last_5_occupancy=14.5, occupancy=15.5)
    print(trainrecord)
    return trainrecord


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

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
    # Create the database and the database table
    db.create_all()

    # Insert user data
    trainrecord1 = TrainData('2019-09-14 13:32:00+00:00', 'TEST_ID', 1.13, 6.66667, 14.5, 15.5)
    trainrecord2 = TrainData('2019-09-12 13:32:00+00:00', 'ANOTHER_TEST_ID', 1634656.3, 6.66667, 14.5, 15.5)
    db.session.add(trainrecord1)
    db.session.add(trainrecord2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()