from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()

jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=21400, db=0, decode_responses=True)

def initialize_db(app) -> None:
    db.init_app(app)


def create_db() -> None:
    db.create_all()
