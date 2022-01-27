import os

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    try:
        launch_mode = os.environ["FLASK_ENV"]
    except KeyError:
        launch_mode = None
    possible_launch_mode_values = ("PROD", "DEV", "TEST")
    if launch_mode not in possible_launch_mode_values:
        raise ValueError(
            "Expected value in '{}' for FLASK_ENV environment variable. Got '{}' instead.".format(
                possible_launch_mode_values[:], launch_mode
            )
        )
    elif launch_mode == "PROD":
        app.config.from_object("flask_config.ProductionConfig")
    elif launch_mode == "DEV":
        app.config.from_object("flask_config.DevelopmentConfig")
    elif launch_mode == "TEST":
        app.config.from_object("flask_config.TestingConfig")

    # apply the blueprints to the app
    from flaskapp.views import views

    app.register_blueprint(views.bp)

    return app
