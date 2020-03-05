import config
import os

class DevelopmentConfig:
    # Flask
    DEBUG = True
    SECRET_KEY = os.urandom(24) #追記

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(**{
        'user': config.MYSQL_USERNAME,
        'password': config.MYSQL_PASSWORD,
        'database': config.MYSQL_DATABASE_NAME,
        'host': 'localhost',
        'port': '3306'
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


Config = DevelopmentConfig
