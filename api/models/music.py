from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from api.db import db


class MusicRequestModel(db.Model):
    __tablename__ = 'music'

    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.String(80))
    release_date = db.Column(db.Date)
    artist = db.Column(db.String(80))
    album = db.Column(db.String(80))
    deezer_id = db.Column(db.Integer)
    music_type = db.Column(db.String(80))
    cover = db.Column(db.String(160))
    request_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(
        self,
        deezer_id: int,
        user: int,
        track: Optional[str] = None,
        release_date: Optional[date] = None,
        artist: Optional[str] = None,
        album: Optional[str] = None,
        music_type: Optional[str] = None,
        cover: Optional[str] = None,
    ) -> None:
        self.track = track
        self.user_id = user
        self.release_date = release_date
        self.artist = artist
        self.album = album
        self.deezer_id = deezer_id
        self.music_type = music_type
        self.cover = cover
        self.request_date = datetime.today()

    def json(self) -> dict:
        """Returns the database entry as a json formatted dictionary.

        Returns:
            dict: music details in json format
        """
        return {
            'id': self.id,
            'track': self.track,
            'release_date': str(self.release_date),
            'artist': self.artist,
            'album': self.album,
            'deezer_id': self.deezer_id,
            'type': self.music_type,
            'cover': self.cover,
            'user_id': self.user_id,
            'request_date': str(self.request_date),
        }

    @classmethod
    def find_by_deezer_id(cls, deezer_id: int) -> MusicRequestModel | None:
        """Queries music entry by deezer id

        Args:
            deezer_id (int): Deezer id to query with

        Returns:
            MusicRequestModel | None: Queried music object if found else None
        """
        return cls.query.filter_by(deezer_id=deezer_id).first()

    @classmethod
    def find_all(cls) -> list[MusicRequestModel]:
        """Retrieves all the requests in music_requests table.

        Returns:
            list: All music requests.
        """
        return cls.query.all()

    @classmethod
    def find_all_by_user(cls, user_id: int) -> list[MusicRequestModel]:
        """Retrieves all requests by the given user.

        Args:
            user_id (int): User's id to query with.

        Returns:
            list: All music requests.
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
