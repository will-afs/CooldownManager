"""Flask configuration."""
import os

from dotenv import load_dotenv
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__)


class Config:
    """Base config."""

    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProductionConfig(Config):
    FLASK_ENV = "PROD"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    FLASK_ENV = "DEV"
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    FLASK_ENV = "TEST"
    DEBUG = True
    TESTING = True
