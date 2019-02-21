from flask import request, flash
from cube.activities.upload import *

activity = Blueprint('activity', __name__)


##########################################################
@activity.route("/cons", methods=['GET', 'POST'])
def cons():
    if request.method == 'POST':
        uploadHandler = UploadHandler(request)
        uploadHandler.report_input_params()
        #uploadHandler.upload()
        # if there are problems, render warning page
        if not uploadHandler.input_ok():
            flash(uploadHandler.errmsg, 'error')
            return render_template('cons.html', storage='bottle')
        # upload_file()

        return render_template('home.html', storage='bottle')
    else:
        return render_template('cons.html', storage='bottle')


@activity.route("/spec", methods=['GET', 'POST'])
def spec():
    return render_template('spec.html', storaage='can')


