from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
api = Api()

def create_app(config_filename=None, **kwargs):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    api.init_app(app)

    from project import models


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.recipes import recipes_blueprint

    app.register_blueprint(recipes_blueprint)


def init_celery(celery, app):
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    #os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ConextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ConextTask
