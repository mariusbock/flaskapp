FROM python:latest

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]
CMD ["run.py"]