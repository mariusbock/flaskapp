from project import db


class TrainData(db.Model):
    __tablename__ = 'TrainData'
    timestamp = db.Column(db.DateTime,
                          primary_key=True)
    id = db.Column(db.String,
                   primary_key=True,
                   nullable=False)
    last_occupancy = db.Column(db.Float)
    last_1_occupancy = db.Column(db.Float)
    last_5_occupancy = db.Column(db.Float)
    occupancy = db.Column(db.Float)
    """
        def __repr__(self):
        return self.timestamp, self.id, self.last_occupancy, self.last_1_occupancy, self.last_5_occupancy, self.occupancy

    def __str__(self):
        template = '{0.timestamp} {0.id} {0.last_occupancy} {0.last_1_occupancy} {0.last_5_occupancy} {0.occupancy}'
        return template.format(self)
    """

    def __init__(self, timestamp, id, last_occupancy, last_1_occupancy, last_5_occupancy,
                 occupancy):
        self.timestamp = timestamp
        self.id = id
        self.last_occupancy = last_occupancy
        self.last_1_occupancy = last_1_occupancy
        self.last_5_occupancy = last_5_occupancy
        self.occupancy = occupancy
