import os

from flask import render_template, request,  redirect,  flash, url_for, Blueprint
from cube.config import Config
from werkzeug.utils import secure_filename

activity = Blueprint('activity', __name__)


##########################################################
@activity.route("/cons", methods=['GET', 'POST'])
def cons():
    if request.method == 'POST':
        qry_name = request.form['qry_nm']
        method = request.form['method']
        #file_name =  request.form['fnm']
        #processed_text = text.upper()
        print (">>>>>>>>>>  form  ", request.form)
        print (">>>>>>>>>>  qry name ", qry_name)
        print (">>>>>>>>>>  method ", method)
        print (">>>>>>>>>>  upload folder ", Config.UPLOAD_FOLDER)
        upload_file()
        return render_template('home.html', storage='bottle')
    else:
        return render_template('cons.html', storage='bottle')


@activity.route("/spec", methods=['GET', 'POST'])
def spec():
    return render_template('spec.html', storaage='can')



##########################################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def upload_file():
    flash('uploading')
    print ("************* in upload_file()")
    # check if the post request has the file part
    if 'fnm' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['fnm']
    print ("*************  " + file.filename)
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print ("************* saving")
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        #return redirect(url_for('uploaded_file', filename=filename))

    return
