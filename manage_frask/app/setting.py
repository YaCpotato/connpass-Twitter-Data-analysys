from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

dialect = "mysql"
driver = "mysqldb"
username = os.environ.get("MYSQL_USERNAME")
password = os.environ.get("MYSQL_PASSWORD")
host = "localhost"
port = "3306"
database = os.environ.get("MYSQL_DATABASE_NAME")
charset_type = "utf8mb4"
db_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset={charset_type}"

# DB接続するためのEngineインスタンス
ENGINE = create_engine(db_url, echo=True)

# DBに対してORM操作するときに利用
# Sessionを通じて操作を行う
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)

# 各modelで利用
# classとDBをMapping
Base = declarative_base()