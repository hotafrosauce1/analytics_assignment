
from sqlalchemy import Column, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP

Base = declarative_base()

# ORM model for health_metrics table
class HealthMetric(Base):
    __tablename__ = 'health_metrics'

    user_id = Column(Integer, primary_key = True, index = True)
    timestamp = Column(TIMESTAMP(timezone = True), server_default = func.now(), primary_key = True, index = True)
    heart_rate = Column(Integer)
    steps = Column(Integer)
    calories = Column(Float)