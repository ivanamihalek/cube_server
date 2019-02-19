from flask import Flask
from cube.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    from cube.main.routes import main
    from cube.errors.handlers import errors
    from cube.activities.routes import activity
    from cube.help.routes import help

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(activity)
    app.register_blueprint(help)

    return app


