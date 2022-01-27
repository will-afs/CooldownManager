import os

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    try:
        launch_mode = os.environ["FLASK_ENV"]
    except KeyError:
        launch_mode = None
    possible_launch_mode_values = ("prod", "dev", "test")
    if launch_mode not in possible_launch_mode_values:
        raise ValueError(
            "Expected value in '{}' for FLASK_ENV environment variable. Got '{}' instead.".format(
                possible_launch_mode_values[:], launch_mode
            )
        )
    elif launch_mode == "prod":
        app.config.from_object("flask_config.ProdConfig")
    elif launch_mode == "dev":
        app.config.from_object("flask_config.DevConfig")
    elif launch_mode == "test":
        app.config.from_object("flask_config.TestConfig")

    # apply the blueprints to the app
    from flaskapp.views import views

    app.register_blueprint(views.bp)

    return app
