import os
from datetime import timedelta


class Config:
    """Set Flask configuration from environment variables."""

    # General Config
    ACCESS_EXPIRES = timedelta(hours=6)  # TTL for jwt tokens
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database Config
    uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # JWT Configuration
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
