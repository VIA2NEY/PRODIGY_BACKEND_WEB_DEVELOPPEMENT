import os
# from dotenv import load_dotenv

# load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Settings:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')


settings = Settings()