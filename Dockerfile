FROM python:3.6-alpine

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY flaskapp project

ENTRYPOINT ["python"]
CMD ["__init__.py"]