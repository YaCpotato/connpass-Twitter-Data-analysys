from sqlalchemy import Column, Text, Integer, BigInteger, String, DateTime, Sequence
from setting import ENGINE, Base
from datetime import datetime
import sys


class Tweet(Base):
	"""
	TweetModel
	"""
	__tablename__ = 'tweets'
	tweet_id = Column(BigInteger, primary_key=True)
	content = Column(Text)
	date = Column(DateTime, default=datetime.now, nullable=True)
	inpression = Column(Integer,nullable=True)
	engagement = Column(Integer,nullable=True)
	retweet = Column(Integer,nullable=True)
	reply = Column(Integer,nullable=True)
	like = Column(Integer,nullable=True)
	profile_click = Column(Integer,nullable=True)
	url_click = Column(Integer,nullable=True)
	hashtag_click = Column(Integer,nullable=True)
	detail_click = Column(Integer,nullable=True)

def main(args):
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)
