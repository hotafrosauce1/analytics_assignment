from pydantic import BaseModel
from datetime import datetime

class HealthMetricPOST(BaseModel):
    user_id: int
    timestamp: datetime
    heart_rate: int
    steps: int
    calories: float