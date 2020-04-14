from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Constants

# API and local DB object
api = Api()
local_db = SQLAlchemy()


def create_app(config, celery):
    """
    Function that is called to start the Flask application.
    :param config: Config object that holds all configurations (see config.py for sample configurations)
    :param celery: Celery object that is passed to the application
    :return: running instance of application
    """
    app = Flask(__name__, instance_relative_config=True)
    # Set CORS policy of application
    CORS(app)
    # Configure app using config object
    app.config.from_object(config)
    # Initialize all extensions and Celery
    initialize_extensions(app)
    init_celery(celery, app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    """
    Function that initializes all extensions used within the application
    :param app: application that you want to initialize the extensions for.
    """
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    api.init_app(app)
    local_db.init_app(app)


def register_blueprints(app):
    """
    Registers all routes with the application
    :param app: application for which blueprints to register for
    """
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.recipes import recipes_blueprint

    app.register_blueprint(recipes_blueprint)


def init_celery(celery, app):
    """
    Initializes celery instance with using configurations from constants file
    :param celery: Celery object to be initialized
    :param app: Underlying application
    """
    app.config['CELERY_BROKER_URL'] = Constants.REDIS_SERVER
    app.config['CELERY_RESULT_BACKEND'] = Constants.REDIS_SERVER

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ConextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ConextTask
