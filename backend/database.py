import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
from sqlalchemy.orm import sessionmaker, declarative_base

# Get DATABASE_URL from env, default to SQLite
# Render/Heroku use 'postgres://', but SQLAlchemy requires 'postgresql://'
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sec_data.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Check args: SQLite needs check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Create the tables in the database."""
    # Import models to ensure they are registered with Base
    from models import Company, FinancialMetric
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Get a new database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
