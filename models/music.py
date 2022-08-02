from __future__ import annotations
from datetime import datetime, date
from db import db
from typing import Optional


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
    store = db.relationship('UserModel')

    def __init__(self, deezer_id, track: Optional[str] = None, release_date: Optional[date] = None,
                 artist: Optional[str] = None, album: Optional[str] = None, music_type: Optional[str] = None,
                 cover: Optional[str] = None) -> None:
        self.track = track
        self.release_date = release_date
        self.artist = artist
        self.album = album
        self.deezer_id = deezer_id
        self.music_type = music_type
        self.cover = cover
        self.request_date = datetime.today()

    def json(self) -> dict:
        return {'id': self.id,
                'track': self.track,
                'release_date': str(self.release_date),
                'artist': self.artist,
                'album': self.album,
                'deezer_id': self.deezer_id,
                'type': self.music_type,
                'cover': self.cover,
                'user_id': self.user_id,
                'request_date': str(self.request_date)}

    @classmethod
    def find_by_deezer_id(cls, deezer_id: int) -> MusicRequestModel | None:
        return cls.query.filter_by(deezer_id=deezer_id).first()

    @classmethod
    def find_all(cls) -> list[MusicRequestModel]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
