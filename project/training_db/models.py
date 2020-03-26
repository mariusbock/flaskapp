from project import local_db


class TrainedModel:
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
