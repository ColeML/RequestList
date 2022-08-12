import os
from urllib.parse import urlparse

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

url = urlparse(os.environ.get('REDIS_URL'))
jwt_redis_blocklist = redis.StrictRedis(
    url.hostname,
    url.port,
    db=0,
    username=url.username,
    password=url.password,
    decode_responses=True
)


def initialize_db(app: Flask) -> None:
    """Initializes the database.

    Args:
        app: Flask app object
    """
    db.init_app(app)


def create_db() -> None:
    """Creates database tables from Models"""
    db.create_all()
