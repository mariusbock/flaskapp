from project import db

class Status:

    __tablename__ = "status"
    id = db.Column(db.String, primary_key=True)
    occupancy = db.Column(db.Float)
    vehicle_flow = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    def __init__(self, id, timestamp, occupancy, vehicle_flow):
        self.id = id
        self.occupancy = occupancy
        self.vehicle_flow = vehicle_flow
        self.timestamp = timestamp
