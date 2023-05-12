from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from extensions import db

class Integrations(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    access_token = Column(String(255), nullable=False)
    refresh_token= Column(String(255), nullable=False)
    expiry = Column(DateTime, default=datetime.utcnow)

