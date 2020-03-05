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