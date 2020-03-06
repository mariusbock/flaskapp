FROM python:3.6-slim-buster

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN apt update &&  apt install -y && apt install libgomp1
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["python"]
CMD ["run.py"]