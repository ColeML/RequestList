from __future__ import annotations

from api.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    user_type = db.Column(db.String(25))

    def __init__(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str,
    ) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = UserLevels.USER

    def json(self) -> dict:
        """Returns the database entry as a json formatted dictionary

        Returns:
            dict: User details in json format
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first': self.first_name,
            'last': self.last_name,
        }

    def save_to_db(self) -> None:
        """Writes the entry to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Removes the entry from the database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> UserModel | None:
        """Queries for the user by username

        Args:
            username (str): Username to query with

        Returns:
            UserModel | None: User's UserModel object or None if not found.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id: int) -> UserModel | None:
        """Queries for the user by user id

        Args:
            user_id (int): User id to query with

        Returns:
            UserModel | None: User's UserModel object or None if not found.
        """
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_all(cls) -> list[UserModel]:
        """Retrieves all users in users table"""
        return cls.query.all()


class UserLevels:
    ADMIN = 0
    USER = 1
