from __future__ import annotations
from db import db


class ShowRequestModel(db.Model):
    __tablename__ = 'show_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    imdb_id = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store = db.relationship('UserModel')

    def __init__(self, title: str, year: int, imdb_id: str) -> None:
        self.title = title
        self.year = year
        self.imdb_id = imdb_id

    def json(self) -> dict:
        return {'id': self.id, 'title': self.title, 'year': self.year, 'imdb_id': self.imdb_id}

    @classmethod
    def find_by_id(cls, imdb_id: str) -> ShowRequestModel:
        return cls.query.filter_by(imdb_id=imdb_id).first()

    @classmethod
    def find_all(cls) -> list[ShowRequestModel]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
