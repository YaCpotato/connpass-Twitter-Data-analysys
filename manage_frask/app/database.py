from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #追記

db = SQLAlchemy()


def initialize_database(app):
    db.init_app(app)
    Migrate(app, db) #追記
