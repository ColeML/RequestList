from __future__ import annotations

from datetime import date
from typing import Optional

from api.db import db


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

    def __init__(
        self,
        title: str,
        authors: list[str],
        user: int,
        subtitle: Optional[str] = None,
        release_date: Optional[date] = None,
        isbn_13: Optional[str] = None,
        isbn_10: Optional[int] = None,
        book_format: Optional[str] = None,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.release_date = release_date
        self.isbn_13 = isbn_13
        self.isbn_10 = isbn_10
        self.user_id = user
        self.book_format = book_format

    def json(self) -> dict:
        """Returns the database entry as a json formatted dictionary.

        Returns:
            dict: book's details in json format
        """
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'authors': self.authors,
            'release_date': str(self.release_date),
            'isbn_10': self.isbn_10,
            'isbn_13': self.isbn_13,
            'book_format': self.book_format,
        }

    @classmethod
    def find_by_isbn(
            cls,
            isbn: str,
            book_format: str) \
            -> BookRequestModel | None:
        """Queries book entry by isbn and book format

        Args:
            isbn (str): ISBN10 or ISBN13 to query with
            book_format (str): Desired book format - (ebook, audiobook)

        Returns:
            BookRequestModel | None: Queried book object if found else None
        """
        return cls.query.filter(
            cls.book_format == book_format,
            (cls.isbn_13 == isbn) | (cls.isbn_10 == isbn),
        ).first()

    @classmethod
    def find_all(cls) -> list[BookRequestModel]:
        """Retrieves all the requests in book_requests table.

        Returns:
            list: All book requests.
        """
        return cls.query.all()

    @classmethod
    def find_all_by_user(cls, user_id: int) -> list[BookRequestModel]:
        """Retrieves all requests by the given user.

        Args:
            user_id (int): User's id to query with.

        Returns:
            list: All book requests.
        """
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self) -> None:
        """Writes the entry to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Removes the entry from the database."""
        db.session.delete(self)
        db.session.commit()
