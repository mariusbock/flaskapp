from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Constants

training_db = create_engine(Constants.TRAINING_DATABASE_URI)
api = Api()
local_db = SQLAlchemy()


def create_app(config, celery):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(config)
    initialize_extensions(app)
    init_celery(celery, app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    api.init_app(app)
    local_db.init_app(app)



def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.recipes import recipes_blueprint

    app.register_blueprint(recipes_blueprint)


def init_celery(celery, app):
    app.config['CELERY_BROKER_URL'] = Constants.REDIS_SERVER
    app.config['CELERY_RESULT_BACKEND'] = Constants.REDIS_SERVER

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ConextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ConextTask
