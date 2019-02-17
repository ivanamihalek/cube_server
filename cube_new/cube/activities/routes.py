from flask import render_template,  Blueprint

activity = Blueprint('activity', __name__)


@activity.route("/cons")
def cons():
    return render_template('cons.html', storage='bottle')


@activity.route("/spec")
def spec():
    return render_template('spec.html', storaage='can')

