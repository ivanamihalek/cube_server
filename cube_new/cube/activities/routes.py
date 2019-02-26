from flask import request, flash, Blueprint, render_template
from cube.activities.upload import *
from cube.activities.conservation import *

activity = Blueprint('activity', __name__)


##########################################################
@activity.route("/cons", methods=['GET', 'POST'])
def cons():
    if request.method == 'POST':
        uploadHandler = UploadHandler(request)
        uploadHandler.report_input_params()
        #uploadHandler.upload()
        # if there are problems, render warning page
        if not uploadHandler.filenames_ok():
            flash(uploadHandler.errmsg, 'error')
            return render_template('cons.html')
        uploadHandler.upload_files()
        if not uploadHandler.upload_ok():
            flash(uploadHandler.errmsg, 'error')
            return render_template('cons.html')

        conservationist  = Conservationist(uploadHandler)
        conservationist.run()
        if not conservationist.run_ok:
            flash(uploadHandler.errmsg, 'error')
        return cons_results(uploadHandler.job_id)

    else:
        return render_template('cons.html', storage='bottle')


##########################################################
@activity.route("/cons/<string:job_id>", methods=['POST'])
def cons_results(job_id):
    return render_template('cons_results.html', job_id=job_id)


##########################################################
@activity.route("/spec", methods=['GET', 'POST'])
def spec():
    return render_template('spec.html', storaage='can')

