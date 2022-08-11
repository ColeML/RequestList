from __future__ import annotations
from api.db import db
from typing import Optional
from datetime import date


class BookRequestModel(db.Model):
    __tablename__ = 'book_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    authors = db.Column(db.String(80))
    release_date = db.Column(db.Date)
    isbn_13 = db.Column(db.String(80))
    isbn_10 = db.Column(db.String(80))
    book_format = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(self, title: str, authors: list[str], user: int, subtitle: Optional[str] = None,
                 release_date: Optional[date] = None, isbn_13: Optional[str] = None,
                 isbn_10: Optional[int] = None, book_format: Optional[str] = None) -> None:
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.release_date = release_date
        self.isbn_13 = isbn_13
        self.isbn_10 = isbn_10
        self.user_id = user
        self.book_format = book_format

    def json(self) -> dict:
        return {'id': self.id,
                'title': self.title,
                'subtitle': self.subtitle,
                'authors': self.authors,
                'release_date': str(self.release_date),
                'isbn_10': self.isbn_10,
                'isbn_13': self.isbn_13,
                'book_format': self.book_format}

    @classmethod
    def find_by_isbn(cls, isbn: str, book_format: str) -> BookRequestModel | None:
        return cls.query.filter(cls.book_format == book_format,
                                (cls.isbn_13 == isbn) | (cls.isbn_10 == isbn)).first()

    @classmethod
    def find_all(cls) -> list[BookRequestModel]:
        return cls.query.all()

    @classmethod
    def find_all_by_user(cls, username: str) -> list[BookRequestModel]:
        return cls.query.filter_by(user=username).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
