
from werkzeug.utils import secure_filename
from cube.config import Config
import os, subprocess

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

        self.seq_input_type = None

        self.errmsg = None

    def _allowed_file(self, filename, allowed_extensions):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def _find_seq_input_type(self):
        cmd = "grep  '>' {}/{} ".format(Config.UPLOAD_FOLDER, self.clean_seq_fnm)
        output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
        if len(output)>0:
            self.seq_input_type = 'fasta'
            return
        cmd = "grep  'Name: ' {}/{} ".format(Config.UPLOAD_FOLDER,self.clean_seq_fnm)
        output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
        if len(output)>0:
            self.seq_input_type = 'gcg'
            return

    def _ref_seq_ok(self):
        if self.seq_input_type == 'fasta':
            cmd = "grep  '>' {}/{} | grep {}".format(Config.UPLOAD_FOLDER,self.clean_seq_fnm, self.qry_name)
        else:
            cmd = "grep 'Name: '  {}/{} | grep {} ".format(Config.UPLOAD_FOLDER,self.clean_seq_fnm, self.qry_name)
        output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
        return (len(output)>0)

    # before the upload to staging:  are the names reasonable?
    def filenames_ok(self):
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
        # structure file - note that struct file is optional
        if self.struct_file and self.struct_file.filename!='':
            self.clean_struct_fnm = secure_filename(self.struct_file.filename)
            if not self.clean_struct_fnm  or  self.clean_struct_fnm == '':
                 self.errmsg = "Please provide input structure in a file with reasonable name."
                 return False
            if not self._allowed_file(self.clean_struct_fnm, Config.ALLOWED_STRUCTFILE_EXTENSIONS):
                self.errmsg = "Please provide input sequences in a file with one of the extensions: "
                self.errmsg += ", ".join([e for e in Config.ALLOWED_STRUCTFILE_EXTENSIONS])
                return False
        # if we're here, we're ok
        return True

    # check input, and provide  feedback if not ok
    # this is the first round of checking - before moving the files
    # from the staging to the work directory
    def upload_ok(self):
        # is the sequence file format recognizable?
        self._find_seq_input_type()
        if not self.seq_input_type:
            self.errmsg = "Sequence file format not recognized."
            return False

        # if the ref sequence is given, it should be present in the alignment
        if not self._ref_seq_ok():
            self.errmsg  = "{} not found in {}. ".format(self.qry_name, self.clean_seq_fnm)
            self.errmsg += "\nPlease include the reference sequence, or perhaps check the name spelling"
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



