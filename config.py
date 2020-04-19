import os


class Constants:
    """
    Object that holds all constants and routes used within the application.
    """
    """ 
    CONSTANTS
    """
    # NOTE FOR DEPLOYMENT: Change String to localhost if you plan on deploying locally
    FLASK_ADDRESS = "http://134.155.108.171:2000"

    BACKEND_ADDRESS = "http://xAnalyticBackend:8080"
    # NOTE FOR DEPLOYMENT: Change to address of xData if it is deployed somewhere else
    XDATA_ADDRESS = "http://xDataEndpoint:4000"
    REDIS_SERVER = "redis://xAnalyticRedis:6379/0"

    # Change following strings only if you use a different xData Deployment than stated in GitHub.
    # NOTE FOR DEPLOYMENT: Change to address where postGres database is deployed to.
    POSTGRES_DB_ADDRESS = "postGis:5432"
    POSTGRES_USER = "postgres"
    POSTGRES_PW = "root"
    POSTGRES_TRAINING_DB = "Training_Database"

    # URI link to Training Database that is connected to xData
    TRAINING_DATABASE_URI = 'postgres://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW,
                                                                       url=POSTGRES_DB_ADDRESS,
                                                                       db=POSTGRES_TRAINING_DB)

    """
    ROUTES
    """
    BACKEND_UPDATE_REQUEST_STATUS = BACKEND_ADDRESS + "/xtraffic-server/xtraffic-api/flask/update-request-status"
    BACKEND_GET_MOCK_DATA = BACKEND_ADDRESS + "/xtraffic-server/xtraffic-api/flask-dev/get-mock-data"


class Config:
    """
    Object that holds all configurations that can be used to start the application normally.
    """
    # Get the folder of the top-level directory of flaskapp
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    WTF_CSRF_ENABLED = True
    DEBUG = True

    # SQLAlchemy strings used to deploy local Flask DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    """
    Object that holds all configurations that can be used to start the application in a testing environment.
    """
    # Get the folder of the top-level directory of flaskapp
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    DEBUG = True

    # Enable the TESTING flag to disable the error catching during train_request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True

    # SQLAlchemy strings used to deploy local Flask DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.local_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
