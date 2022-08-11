from __future__ import annotations
from api.db import db
from datetime import datetime


class ShowRequestModel(db.Model):
    __tablename__ = 'show_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    imdb_id = db.Column(db.String(80))
    request_date = db.Column(db.DateTime)

    user = db.Column(db.String(40), db.ForeignKey('users.username'))
    users = db.relationship('UserModel')

    def __init__(self, title: str, year: int, imdb_id: str, user: str) -> None:
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.user = user
        self.request_date = datetime.today()

    def json(self) -> dict:
        return {'id': self.id,
                'title': self.title,
                'year': str(self.year),
                'imdb_id': self.imdb_id,
                'user_id': self.user_id,
                'request_date': str(self.request_date)}

    @classmethod
    def find_by_id(cls, imdb_id: str) -> ShowRequestModel:
        return cls.query.filter_by(imdb_id=imdb_id).first()

    @classmethod
    def find_all(cls) -> list[ShowRequestModel]:
        return cls.query.all()

    @classmethod
    def find_all_by_user(cls, username: str) -> list[ShowRequestModel]:
        return cls.query.filter_by(user=username).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
