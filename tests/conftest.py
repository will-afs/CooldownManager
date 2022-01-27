""""This file contains setup functions called fixtures that each test will use"""

import os
import tempfile

import pytest

from flaskapp import create_app


@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "test"  # Equivalent to "export FLASK_ENV=test" in bash

    app = create_app()

    yield app


@pytest.fixture
def client(app):
    # The client fixture calls app.test_client() with the application object created by the app
    # fixture. Tests will use the client to make requests to the application without running the
    #  server.
    return app.test_client()


@pytest.fixture
def create_app_for_tc(app):
    with app.app_context():
        yield app


@pytest.fixture()  #
def test_client(app):
    """A test client for the app."""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def runner(app):
    # The runner fixture is similar to client. app.test_cli_runner() creates a runner that can
    # call the Click commands registered with the application.The runner fixture is similar to
    # client. app.test_cli_runner() creates a runner that can call the Click commands registered
    # with the application.
    return app.test_cli_runner()
