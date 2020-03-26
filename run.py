from project import create_app
from project.celery import celery
from config import TestConfig

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg

app = create_app(config=TestConfig, celery=celery)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
