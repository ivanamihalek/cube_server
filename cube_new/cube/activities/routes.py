from flask import render_template, request,  Blueprint
from cube.config import Config

activity = Blueprint('activity', __name__)



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
        return render_template('home.html', storage='bottle')
    else:
        return render_template('cons.html', storage='bottle')


@activity.route("/spec", methods=['GET', 'POST'])
def spec():

    return render_template('spec.html', storaage='can')

