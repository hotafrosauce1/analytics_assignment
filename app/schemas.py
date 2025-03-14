# app/schemas.py

from pydantic import BaseModel
from datetime import datetime

class HealthMetricCreate(BaseModel):
    user_id: int
    timestamp: datetime
    heart_rate: int
    steps: int
    calories: float