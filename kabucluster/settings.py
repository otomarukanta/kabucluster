import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

TWITTER_LIST_IDS = os.environ.get('TWITTER_LIST_IDS', '').split(',')

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('DB_DATABASE')

def create_engine():
    return sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            'mysql+pymysql',
            username=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_DATABASE
        ),
    echo=True)

def create_session(engine):
    return scoped_session(
        sessionmaker(
            autocommit = False,
            autoflush = True,
            bind = engine
        )
    )

engine = create_engine()
session = create_session(engine)
