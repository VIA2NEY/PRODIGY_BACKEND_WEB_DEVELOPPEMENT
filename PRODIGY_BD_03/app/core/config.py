import os
# from dotenv import load_dotenv

# load_dotenv()

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class Settings:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
        
    # JWT Configuration
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or "super-secret-key-minimum-32-characters"
    ALGORITHM: str = os.environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES') or 60

settings = Settings()