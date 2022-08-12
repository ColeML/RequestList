from __future__ import annotations

from datetime import datetime

from api.db import db


class MovieRequestModel(db.Model):
    __tablename__ = 'movie_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    imdb_id = db.Column(db.String(80))
    request_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(self, title: str, year: int, imdb_id: str, user: int) -> None:
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.user_id = user
        self.request_date = datetime.now()

    def json(self) -> dict:
        """Returns the movies database entry as a json formatted dictionary.

        Returns:
            dict: movie's details in json format
        """
        return {
            'id': self.id,
            'title': self.title,
            'year': str(self.year),
            'imdb_id': self.imdb_id,
            'user_id': self.user_id,
            'request_date': str(self.request_date),
        }

    @classmethod
    def find_by_id(cls, imdb_id: str) -> MovieRequestModel | None:
        """Queries movie entry by imdb_id

        Args:
            imdb_id (str): IMDB id to query with

        Returns:
            MovieRequestModel | None: Queried movie object if found else None
        """
        return cls.query.filter_by(imdb_id=imdb_id).first()

    @classmethod
    def find_all(cls) -> list[MovieRequestModel]:
        """Retrieves all the requests in movie_requests table.

        Returns:
            list: All book requests.
        """
        return cls.query.all()

    @classmethod
    def find_all_by_user(cls, user_id: int) -> list[MovieRequestModel]:
        """Retrieves all requests by the given user.

        Args:
            user_id (int): User's id to query with.

        Returns:
            list: user's movie requests.
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
