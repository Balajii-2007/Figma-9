"""
config.py — Environment-based configuration classes.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY         = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_NAME           = "Sports Event Registration"


class DevelopmentConfig(BaseConfig):
    DEBUG              = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'sports.db'}"


class TestingConfig(BaseConfig):
    TESTING            = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED   = False


class ProductionConfig(BaseConfig):
    DEBUG              = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'sports.db'}")


config_map = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
}
