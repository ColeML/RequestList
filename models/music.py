from __future__ import annotations
from db import db


class MusicRequestModel(db.Model):
    __tablename__ = 'music'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store = db.relationship('UserModel')

    def __init__(self, title, year) -> None:
        self.title = title
        self.year = year

    def json(self) -> dict:
        return {'id': self.id, 'title': self.title, 'year': self.year, 'user_id': self.user_id}

    @classmethod
    def find_by_title(cls, title: str, year: int) -> MusicRequestModel | None:
        return cls.query.filter_by(title=title, year=year).first()

    @classmethod
    def find_all(cls) -> list[MusicRequestModel]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
