from __future__ import annotations
from api.db import db


class BookRequestModel(db.Model):
    __tablename__ = 'book_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    authors = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    isbn_13 = db.Column(db.Integer)
    isbn_10 = db.Column(db.Integer)
    book_format = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store = db.relationship('UserModel')

    def __init__(self, title: str, subtitle: str, authors: str, date: str,
                 isbn_13: int, isbn_10: int, book_format: str) -> None:
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.date = date
        self.isbn_13 = isbn_13
        self.isbn_10 = isbn_10
        self.book_format = book_format

    def json(self) -> dict:
        return {'id': self.id,
                'title': self.title,
                'subtitle': self.subtitle,
                'authors': self.authors,
                'date': self.date,
                'isbn_10': self.isbn_10,
                'isbn_13': self.isbn_13,
                'book_format': self.book_format}

    @classmethod
    def find_by_title(cls, title: str, year: int) -> BookRequestModel | None:
        return cls.query.filter_by(title=title, year=year).first()

    @classmethod
    def find_by_isbn13(cls, isbn: str) -> BookRequestModel | None:
        return cls.query.filter_by(isbn_13=isbn)

    @classmethod
    def find_by_isbn10(cls, isbn: str) -> BookRequestModel | None:
        return cls.query.filter_by(isbn_10=isbn)

    @classmethod
    def find_all(cls) -> list[BookRequestModel]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
