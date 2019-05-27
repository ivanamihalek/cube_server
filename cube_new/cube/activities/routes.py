from flask import request, flash, Blueprint, render_template
from cube.activities.upload import *
from cube.activities.conservation import *

activity = Blueprint('activity', __name__)


##########################################################
@activity.route("/cons", methods=['GET', 'POST'])
def cons():
	if request.method == 'POST':
		upload_handler = UploadHandler(request)
		upload_handler.report_input_params()
		#upload_handler.upload()
		# if there are problems, render warning page
		if not upload_handler.filenames_ok():
			flash(upload_handler.errmsg, 'error')
			return render_template('cons.html')
		upload_handler.upload_files()
		if not upload_handler.upload_ok():
			flash(upload_handler.errmsg, 'error')
			return render_template('cons.html')

		conservationist = Conservationist(upload_handler)
		conservationist.run()
		if not conservationist.run_ok:
			flash(upload_handler.errmsg, 'error')
		if conservationist.warn:
			flash(conservationist.warn, 'warning')
		return cons_results(conservationist)

	else:
		return render_template('cons.html', storage='bottle')


##########################################################
@activity.route("/cons/<string:job_id>", methods=['POST'])
def cons_results(conservationist):
	return render_template('cons_results.html', results_handler=conservationist)


##########################################################
@activity.route("/spec", methods=['GET', 'POST'])
def spec():
	if request.method == 'POST':
		upload_handler = UploadHandler(request)
		upload_handler.report_input_params()
	return render_template('spec.html', storage='can')

