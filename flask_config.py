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


class ProdConfig(Config):
    FLASK_ENV = "prod"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = "dev"
    DEBUG = True
    TESTING = False


class TestConfig(Config):
    FLASK_ENV = "test"
    DEBUG = True
    TESTING = True
