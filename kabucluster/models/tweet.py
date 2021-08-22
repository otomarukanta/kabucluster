from sqlalchemy import Column, BigInteger, String, DateTime

from kabucluster.models.base import Base, TimestampMixin

class Tweet(TimestampMixin, Base):
    __tablename__ = 'tweet'

    id = Column(BigInteger, primary_key=True)
    tweeted_at = Column(DateTime)
    user_id = Column(BigInteger)
    user_name = Column(String(length=200))
    text = Column(String(length=500))