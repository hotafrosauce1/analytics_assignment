from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL, echo = False)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# Create a session instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()