from flask import Flask
from cube.config import Config
import os, subprocess

#####################################
def check_dependencies():
    print (" = Dependencies check:")
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
    print ("\tDependencies ok")

    print (" = Libs check:")
    for dep, path in Config.LIBS.items():
        if not os.path.exists(path):
            print(path, "not found")
            exit(1)
        elif os.path.getsize(path)==0:
            print(path, "is empty")
            exit(1)
    print ("\tLibs ok")

    print (" = Directory check:")
    for dirpath in [Config.UPLOAD_PATH, Config.WORK_PATH]:
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        if not os.path.exists(dirpath):
            print(dirpath, "not found and could not be made")
            exit(1)
    for dirpath in [Config.SCRIPTS_PATH]:
        if not os.path.exists(dirpath):
            print(dirpath, "not found ")
            exit(1)
    print("\tdirectories ok")

    print(" = Scripts check:")
    for script in Config.SCRIPTS.values():
        fullpath = "{}/{}".format(Config.SCRIPTS_PATH, script)
        if not os.path.exists(fullpath):
            print (fullpath, "not found")
            exit()
    print("\tscripts ok")

    print(" = Perl module check:")
    for module in Config.PERL_MODULES:
        cmd = "perl -e 'use %s'" % module
        process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if process.returncode!=0:
            print(module, "not found")
            exit()
    print("\tperl modules ok")


##########################################
def create_app():
    app = Flask(__name__)

    Config.APP_PATH = app.root_path
    Config.WORK_PATH = "{}/static/{}".format(Config.APP_PATH,Config.WORK_DIRECTORY)
    Config.SCRIPTS_PATH  = "{}/{}".format(Config.APP_PATH, Config.SCRIPTS_PATH)

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


