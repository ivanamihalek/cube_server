from flask import Flask
from cube.config import Config
import os

def check_dependencies():
    print (" = Dependency check:")
    for dep, path in Config.DEPENDENCIES.items():
        if not os.path.exists(path):
            print(path, "not found")
            exit(1)
        elif os.path.getsize(path)==0:
            print(path, "is empty")
            exit(1)
        elif not os.access(path, os.X_OK):
            print(path, "not executable")
            exit(1)
    print ("\tdependencies ok")

def create_app():
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


