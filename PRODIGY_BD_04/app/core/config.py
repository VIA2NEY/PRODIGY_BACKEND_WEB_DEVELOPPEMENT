import os
from utils import load_env_file

load_env_file()

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class Settings:

    SECRET_KEY: str = os.environ.get('SECRET_KEY') or "super-secret-key-minimum-32-characters"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
        
    # JWT Configuration
    ALGORITHM: str = os.environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES= int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')) or 60

    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_TTL_USERS: int = int(os.getenv("REDIS_TTL_USERS", 120))

settings = Settings()