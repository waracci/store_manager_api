"""App module: sets the configuration for the flask application"""

# Third party imports
from flask import Flask
from instance.config import app_configuration


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    app.config.from_object(app_configuration[config_name])
    app.config.from_pyfile('config.py')


    return app
