
from flask import render_template,  redirect,   url_for, Blueprint
from werkzeug.utils import secure_filename
from cube.config import Config
import os



class UploadHandler:
    def __init__(self, request):
        self.qry_name    = request.form['qry_nm']
        # careful:  request.files is empty dict if no file selected
        self.seq_file    = request.files['fnm'] if 'fnm' in request.files else None
        # ditto for the checkbox   - if not checked, it does not exist
        self.aligned     = ('aligned' in  request.form)
        self.struct_file = request.files['structure_fnm'] if 'structure_fnm' in request.files else None
        self.chain       = request.form['chain']
        self.method      = request.form['method']

    def _allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    # check input, and provide  feedback if not ok

    def upload_file(self):

        # if user does not a select file, browser will
        # submit an empty part without filename
        if self.seq_file.filename == '':
            print('No selected file')
            return "empty fnm"
        if self.seq_file and self._allowed_file(self.seq_file.filename):
            filename = secure_filename(self.seq_file.filename)
            print ("************* saving")
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

            self.seq_file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            #return redirect(url_for('uploaded_file', filename=filename))

        return

    def report_input_params(self):
        print(">>>>>>>>>>  qry name ", self.qry_name)
        print(">>>>>>>>>>  seq file name ", self.seq_file.filename if self.seq_file else "None")
        print(">>>>>>>>>>  aligned", self.aligned)
        print(">>>>>>>>>>  struct file name ", self.struct_file.filename if self.struct_file else "None")
        print(">>>>>>>>>>  chain ", self.chain)
        print(">>>>>>>>>>  method ", self.method)
        print(">>>>>>>>>>  upload folder ", Config.UPLOAD_FOLDER)



