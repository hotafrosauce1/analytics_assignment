import logging

from celery import Celery
from sqlalchemy.exc import IntegrityError
from app.config import REDIS_BROKER_URL
from app.database import SessionLocal
from app.models import HealthMetric

celery = Celery(
    'tasks',
    broker = REDIS_BROKER_URL,
    backend = REDIS_BROKER_URL,
)
logger = logging.getLogger(__name__)

@celery.task
def ingest_health_data(data):
    db = SessionLocal()
    try:
        row = HealthMetric(**data)
        db.add(row)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.warning(f'Duplicate entry error: {e}')
    except Exception as e:
        db.rollback()
        logger.error(f'Unexpected database error: {e}', exc_info=True)
    finally:
        db.close()