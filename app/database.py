from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL, echo = False)

# Create a session factory
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()