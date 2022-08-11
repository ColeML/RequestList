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

    def __init__(self, username: str, password: str, first_name: str, last_name: str, email: str) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = UserLevels.USER

    def json(self) -> dict:
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'first': self.first_name,
                'last': self.last_name}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class UserLevels:
    ADMIN = 0
    USER = 1
