from project import local_db

"""
Contains all models for local database
"""


class TrainedModel(local_db.Model):
    """
    Model for saved model record
    """
    __tablename__ = 'savedmodels'
    filename = local_db.Column(local_db.String, primary_key=True)
    timestamp = local_db.Column(local_db.String)
    clientid = local_db.Column(local_db.String)
    requestid = local_db.Column(local_db.String)
    downloadlink = local_db.Column(local_db.String)

    def __init__(self, filename, timestamp, clientid, requestid, downloadlink):
        self.timestamp = timestamp
        self.filename = filename
        self.clientid = clientid
        self.requestid = requestid
        self.downloadlink = downloadlink


class TrainRequest(local_db.Model):
    """
    Model for training request record
    """
    __tablename__ = "requests"
    request_id = local_db.Column(local_db.String, primary_key=True)
    client_id = local_db.Column(local_db.String)
    raw_data = local_db.Column(local_db.String)
    meta_data = local_db.Column(local_db.String)
    request_status = local_db.Column(local_db.String)

    def __init__(self, request_id, client_id, raw_data, meta_data):
        self.request_id = request_id
        self.client_id = client_id
        self.raw_data = raw_data
        self.meta_data = meta_data
        self.request_status = "INITIALIZED"

    def serialize(self):
        return {"request_id": self.request_id,
                "client_id": self.client_id,
                "request_status": self.request_status}


class TrainData(local_db.Model):
    """
    Model for training data record
    """
    __tablename__ = "traindata"
    id = local_db.Column(local_db.String, primary_key=True)
    occupancy = local_db.Column(local_db.Float)
    vehicle_flow = local_db.Column(local_db.Float)
    timestamp = local_db.Column(local_db.DateTime)

    def __init__(self, id, timestamp, occupancy, vehicle_flow):
        self.id = id
        self.occupancy = occupancy
        self.vehicle_flow = vehicle_flow
        self.timestamp = timestamp


local_db.create_all()
local_db.session.commit()
