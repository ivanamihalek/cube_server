
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

        self.clean_seq_fnm = None
        self.clean_struct_fnm = None

        self.errmsg = None


    def _allowed_file(self, filename, allowed_extensions):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    # check input, and provide  feedback if not ok
    def input_ok(self):
        # seq file
        if not self.seq_file or  self.seq_file.filename == '':
            self.errmsg = "Please provide a file with input sequences."
            return False
        self.clean_seq_fnm = secure_filename(self.seq_file.filename)
        if not self.clean_seq_fnm  or  self.clean_seq_fnm == '':
            self.errmsg = "Please provide input sequences in a file with reasonable name."
            return False
        if not self._allowed_file(self.clean_seq_fnm, Config.ALLOWED_SEQFILE_EXTENSIONS):
            self.errmsg = "Please provide input sequences in a file with one of the extensions: "
            self.errmsg += ", ".join([e for e in Config.ALLOWED_SEQFILE_EXTENSIONS])
            return False

        # structure file - not struct file is optional
        if self.struct_file and self.struct_file.filename!='':
            self.clean_struct_fnm = secure_filename(self.struct_file.filename)
            if not self.clean_struct_fnm  or  self.clean_struct_fnm == '':
                 self.errmsg = "Please provide input structure in a file with reasonable name."
                 return False
            if not self._allowed_file(self.clean_struct_fnm, Config.ALLOWED_STRUCTFILE_EXTENSIONS):
                self.errmsg = "Please provide input sequences in a file with one of the extensions: "
                self.errmsg += ", ".join([e for e in Config.ALLOWED_STRUCTFILE_EXTENSIONS])
                return False
        return True


    def upload_files(self):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        if self.clean_seq_fnm:
            print ("************* saving", self.clean_seq_fnm)
            self.seq_file.save(os.path.join(Config.UPLOAD_FOLDER, self.clean_seq_fnm))
        if self.clean_struct_fnm:
            print ("************* saving", self.clean_struct_fnm)
            self.struct_file.save(os.path.join(Config.UPLOAD_FOLDER, self.clean_struct_fnm))
        return



    def report_input_params(self):
        print(">>>>>>>>>>  qry name ", self.qry_name)
        print(">>>>>>>>>>  seq file name ", self.seq_file.filename if self.seq_file else "None")
        print(">>>>>>>>>>  aligned", self.aligned)
        print(">>>>>>>>>>  struct file name ", self.struct_file.filename if self.struct_file else "None")
        print(">>>>>>>>>>  chain ", self.chain)
        print(">>>>>>>>>>  method ", self.method)
        print(">>>>>>>>>>  upload folder ", Config.UPLOAD_FOLDER)



