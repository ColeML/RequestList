import os


class Config:
    """ Set Flask configuration from .env file. """

    # General Config
    SECRET_KEY = "temp"  # TODO move to .env (os.environ.get('SECRET_KEY'))

    # Database Config
    uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
