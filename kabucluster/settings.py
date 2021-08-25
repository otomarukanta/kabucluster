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
DB_PORT = os.environ.get('DB_PORT', 3306)

NEOLOGD_PATH = os.environ.get('NEOLOGD_PATH')
STOPWORDS_PATH = os.environ.get('STOPWORDS_PATH', './stopwords.txt')
TICKERS_PATH = os.environ.get('TICKERS_PATH', './tickers.csv')

def create_engine():
    return sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            'mysql+pymysql',
            username=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_DATABASE,
            port=DB_PORT
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
session = create_session(engine) # type: sqlalchemy.orm.scoped_session
