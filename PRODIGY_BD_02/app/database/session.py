
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer le moteur de base de données
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=300
)

# Factory de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/database/base.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
