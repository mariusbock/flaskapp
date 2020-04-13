import os


class Constants:
    # Change String to address of server
    FLASK_ADDRESS = "http://localhost:2000"

    BACKEND_ADDRESS = "http://xAnalyticBackend:8080"
    XDATA_ADDRESS = "http://xDataEndpoint:4000"
    REDIS_SERVER = "redis://xAnalyticRedis:6379/0"

    POSTGRES_DB_ADDRESS = "postGis:5432"
    POSTGRES_USER = "postgres"
    POSTGRES_PW = "root"
    POSTGRES_TRAINING_DB = "Training_Database"

    TRAINING_DATABASE_URI = 'postgres://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW,
                                                                       url=POSTGRES_DB_ADDRESS,
                                                                       db=POSTGRES_TRAINING_DB)

    """
    ROUTES BACKEND
    """
    BACKEND_UPDATE_REQUEST_STATUS = BACKEND_ADDRESS + "/xtraffic-server/xtraffic-api/flask/update-request-status"
    BACKEND_GET_MOCK_DATA = BACKEND_ADDRESS + "/xtraffic-server/xtraffic-api/flask-dev/get-mock-data"


class Config:
    # Get the folder of the top-level directory of this flaskapp
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    WTF_CSRF_ENABLED = True
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    # Get the folder of the top-level directory of this flaskapp
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    DEBUG = True

    # Enable the TESTING flag to disable the error catching during train_request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.local_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
