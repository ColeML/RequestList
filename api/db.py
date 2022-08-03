from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_db(app) -> None:
    db.init_app(app)


def create_db() -> None:
    db.create_all()
