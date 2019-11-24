from project import db

class Status:

    __tablename__ = "status"
    id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime)
    occupancy = db.Column(db.Float)
    vehicle_flow = db.Column(db.Float)

    def __init__(self, id, timestamp, occupancy, vehicle_flow):
        self.id = id
        self.timestamp = timestamp
        self.occupancy = occupancy
        self.vehicle_flow = vehicle_flow
