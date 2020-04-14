FROM python:3.6-slim-buster

WORKDIR /flask-app

# copy requirements file and install all packages (as well as additional ones) needed for application
COPY requirements.txt requirements.txt
RUN apt update &&  apt install -y && apt install libgomp1
RUN pip install --no-cache-dir -r requirements.txt

# copy all other project files
COPY . .

# run application
CMD ["python", "-u", "run.py"]