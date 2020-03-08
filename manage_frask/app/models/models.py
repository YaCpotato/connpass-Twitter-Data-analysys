from sqlalchemy import Column, Text, Integer, BigInteger, String, DateTime, Sequence
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