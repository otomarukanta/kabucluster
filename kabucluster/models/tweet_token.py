from sqlalchemy import Column, BigInteger, String, DateTime

from kabucluster.models.base import Base, TimestampMixin

class TweetToken(TimestampMixin, Base):
    __tablename__ = 'tweet_token'

    id = Column(BigInteger, primary_key=True)
    tweet_id = Column(BigInteger)
    tweeted_at = Column(DateTime)
    user_id = Column(BigInteger)
    screen_name = Column(String(length=200))
    token = Column(String(length=100))
    code = Column(String(length=4))