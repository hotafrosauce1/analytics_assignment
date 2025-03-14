from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import models, schemas
from app.database import engine, get_db
from app.celery_worker import ingest_health_data

# Create the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post('/ingest')
def ingest_data(data: schemas.HealthMetricPOST):
    # Queue the data ingestion task in Redis using Celery
    ingest_health_data.delay(data.model_dump())
    return {'message': 'Data received'}

@app.get('/metrics')
def get_aggregations(
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(get_db)
):
    query = text("""
    SELECT 
        AVG(heart_rate) AS avg_heart_rate, 
        SUM(steps) AS total_steps,
        SUM(calories) AS total_calories
    FROM health_metrics
    WHERE 
        user_id = :user_id AND 
        timestamp >= :start_date AND 
        timestamp <= :end_date
    """)

    # Convert the datetime objects to isoformat strings
    start_date = start_date.isoformat()
    end_date = end_date.isoformat()

    # Execute the query
    try:
        result = db.execute(query, {'user_id': user_id, 'start_date': start_date, 'end_date': end_date}).fetchone()

    # Arbitrary error during query execution
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f'An error occurred: {str(e)}')

    # Check if all columns are None (i.e., no data found)
    if result.avg_heart_rate is None and result.total_steps is None and result.total_calories is None:
        raise HTTPException(status_code = 404, detail = 'No data found for the given user and date range')

    return {
        'avg_heart_rate': float(result.avg_heart_rate),
        'total_steps': int(result.total_steps),
        'total_calories': float(result.total_calories),
    }
