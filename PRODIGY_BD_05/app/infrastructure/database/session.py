from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer le moteur de base de données
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=10, #Pool de 10 connexions
    max_overflow=20, #Overflow jusqu’à 20
    pool_timeout=30, #Timeout 30s
    pool_recycle=1800, #Recycle connexions MySQL (évite “MySQL server has gone away”)
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
