from sqlalchemy import MetaData, Table, Column, Integer, String

from project import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

Base = declarative_base()


class Request(Base):
    __tablename__ = "requests"
    request_id = db.Column(db.String, primary_key=True)
    client_id = db.Column(db.String)
    raw_data = db.Column(db.String)
    meta_data = db.Column(db.String)
    request_status = db.Column(db.String)

    def __init__(self, request_id, client_id, raw_data, meta_data):
        self.request_id = request_id
        self.client_id = client_id
        self.raw_data = raw_data
        self.meta_data = meta_data
        self.request_status = "INITIALIZED"
        save_request_to_db(self)

    def serialize(self):
        return {"request_id":self.request_id,
                "client_id":self.client_id,
                "request_status":self.request_status}

def save_request_to_db(request):
    Session = sessionmaker(bind=db.engine)
    session = Session()
    session.add(request)
    session.commit()

def get_request_by_id(request_id):
    if not db.engine.dialect.has_table(db.engine, "requests"):  # If table don't exist, Create.
        print("CREATING TABLE\n")
        metadata = MetaData(db.engine)
        # Create a table with the appropriate Columns
        Table("requests", metadata,
              Column('request_id', String, primary_key=True, nullable=False),
              Column('client_id', String),
              Column('raw_data', String),
              Column('meta_data', String),
              Column('request_status', String))
              # Implement the creation
        metadata.create_all()

    Session = sessionmaker(bind=db.engine)
    session = Session()
    result = session.query(Request).first()
    return result