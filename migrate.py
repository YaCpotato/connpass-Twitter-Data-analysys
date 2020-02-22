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
	date = Column(DateTime, default=datetime.now, nullable=False)
	inpression = Column(Integer,nullable=False)
	engagement = Column(Integer,nullable=False)
	retweet = Column(Integer,nullable=False)
	reply = Column(Integer,nullable=False)
	like = Column(Integer,nullable=False)
	profile_click = Column(Integer,nullable=False)
	url_click = Column(Integer,nullable=False)
	hashtag_click = Column(Integer,nullable=False)
	detail_click = Column(Integer,nullable=False)

def main(args):
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)
