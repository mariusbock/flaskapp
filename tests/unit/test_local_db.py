"""
This file (test_local_db.py) contains all unit tests for the local database of Flask
"""


def test_new_trained_model(new_trained_model):
    """
    Function that tests whether trained model is created correctly
    :param new_trained_model: new TrainedModel model instance
    :return: test result
    """


def test_new_train_request(new_train_request):
    """
    Function that tests whether training request is created correctly
    :param new_train_request: new TrainRequest model instance
    :return: test result
    """


def test_new_train_data(new_train_data):
    """
    Function that tests whether training record is created correctly
    :param new_train_data: new TrainData model instance
    :return: test result
    """
    print(new_train_data)
    assert new_train_data.timestamp == "2019-10-14 13:32:00+00:00"
    assert new_train_data.id == "18371007[D40a]"
    assert new_train_data.last_occupancy == 16.5
    assert new_train_data.last_1_occupancy == 6.6667
    assert new_train_data.last_5_occupancy == 14.5
    assert new_train_data.occupancy == 15.5


def test_save_train_request_to_db(test_request):
    """
    Function to save_train_request_to_db to database
    :param test_request: request to be saved to DB
    :return: test result
    """


def test_get_train_request_by_id(test_request_id):
    """
    Function that test get_train_request_by_id function
    :param test_request_id: request ID of train request
    :return: test result
    """


def test_get_table_from_db(test_table):
    """
    Function that test get_table_from_db function
    :param test_table: wanted test table
    :return: test result
    """


def test_count_entries_in_table_per_id():
    """
    Function that test count_entries_in_table_per_id function
    :return: test result
    """


def test_delete_old_entries_from_table(test_fields):
    """
    Function that test delete_old_entries_from_table function
    :param test_fields: fields to be deleted
    :return: test result
    """


def test_check_missing_data():
    """
    Function that test check_missing_data function
    :return: test result
    """


def test_send_response_to_server():
    """
    Function that test send_response_to_server function
    :return: test result
    """
