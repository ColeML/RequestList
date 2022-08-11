from flask_sqlalchemy import SQLAlchemy
import os
import redis
from urllib.parse import urlparse


db = SQLAlchemy()

url = urlparse(os.environ.get("REDIS_URL"))
jwt_redis_blocklist = redis.StrictRedis(host=url.hostname,
                                        port=url.port,
                                        username=url.username,
                                        password=url.password,
                                        db=0,
                                        decode_responses=True)


def initialize_db(app) -> None:
    db.init_app(app)


def create_db() -> None:
    db.create_all()
