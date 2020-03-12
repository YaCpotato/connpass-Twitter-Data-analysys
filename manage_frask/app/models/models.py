from sqlalchemy import Column, Text, Integer, BigInteger, String, Date, DateTime, Sequence
from app.database import db
from datetime import datetime
import sys
from flask_login import UserMixin


class User(db.Model, UserMixin): # UserMixin を追記
    __tablename__ = 'users'

    __table_args__ = (
        db.UniqueConstraint('name'),
        db.UniqueConstraint('email'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(15, collation='utf8mb4_general_ci'), nullable=False)
    display_name = Column(String(50, collation='utf8mb4_general_ci'), nullable=False)
    email = Column(String(256, collation='utf8mb4_general_ci'), nullable=False)
    password = Column(String(1024, collation='utf8mb4_general_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, display_name, email, password):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = password
    
class Tweet(db.Model):
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

class Event(db.Model):
    """
    EventModel
    """
    __tablename__ = 'events'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50, collation='utf8mb4_general_ci'), nullable=False)
    event_date = Column(Date, default=datetime.now, nullable=False)
    adstart_date = Column(DateTime, default=datetime.now, nullable=False)
    end_date = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, name, event_date, adstart_date, end_date):
        self.name = name
        self.event_date = event_date
        self.adstart_date = adstart_date
        self.end_date = end_date