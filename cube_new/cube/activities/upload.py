
from werkzeug.utils import secure_filename
from cube.config import Config
import os, subprocess
import string, random

class UploadHandler:
	def __init__(self, request):
		self.qry_name    = request.form['qry_nm']
		# careful:  request.files is empty dict if no file selected
		self.seq_file    = request.files['fnm'] if 'fnm' in request.files else None
		self.original_alignment_path = None
		# ditto for the checkbox   - if not checked, it does not exist
		self.aligned     = ('aligned' in  request.form)
		self.struct_file = request.files['structure_fnm'] if 'structure_fnm' in request.files else None
		self.original_structure_path = None
		self.chain       = request.form['chain']
		self.method      = request.form['method']
		########################################
		self.clean_seq_fnm = None
		self.clean_struct_fnm = None
		########################################
		self.job_id = self._id_generator()
		self.staging_dir = "{}/{}".format(Config.UPLOAD_PATH, self.job_id)
		self.seq_input_type = None
		self.errmsg = None

	def _id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	def _allowed_file(self, filename, allowed_extensions):
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

	############################################################
	#
	def _find_seq_input_type(self):
		cmd = "grep  '>' {} ".format(self.original_alignment_path)
		output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
		if len(output)>0:
			self.seq_input_type = 'fasta'
			return
		cmd = "grep  'Name: ' {} ".format(self.original_alignment_path)
		output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
		if len(output)>0:
			self.seq_input_type = 'gcg'
			return

	def _ref_seq_ok(self):
		if self.seq_input_type == 'fasta':
			cmd = "grep  '>' {} | grep {}".format(self.original_alignment_path, self.qry_name)
		else:
			cmd = "grep 'Name: '  {} | grep {} ".format(self.original_alignment_path, self.qry_name)
		output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
		return (len(output)>0)

	############################################################
	#
	def upload_files(self):
		os.makedirs(self.staging_dir, exist_ok=True)
		if self.clean_seq_fnm:
			print ("************* saving", self.clean_seq_fnm)
			self.original_alignment_path = os.path.join(self.staging_dir, self.clean_seq_fnm)
			self.seq_file.save(self.original_alignment_path)
		if self.clean_struct_fnm:
			print("************* saving", self.clean_struct_fnm)
			self.original_structure_path = os.path.join(self.staging_dir, self.clean_struct_fnm)
			self.struct_file.save(self.original_structure_path)
		return

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
			self.errmsg  = "{} not found in {}.".format(self.qry_name, self.clean_seq_fnm)
			self.errmsg += "\nPlease include the reference sequence, or perhaps check the name spelling"
			return False
		# if the structure is given
		if self.struct_file:
			# which chains do we have in the provided structure file?
			cmd = " awk -F '' '{}' {} | uniq ".format("{print $22}", self.original_structure_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			chains = process.stdout.decode("utf-8").strip().split("\n")
			if self.chain and self.chain != "-":
				# if the chain is specified, the chain should be present in the structure
				if not self.chain in chains:
					self.errmsg = "Chain {} not found in {}.".format(self.chain, self.clean_struct_fnm)
					return False
			else:
				# if there is more than one chain in the structure, the query chain must be specified
				if len(chains) == 1:
					self.chain = chains[0]
				else:
					self.errmsg = "There are {} chains ({}) in {}, but no target chain was specified."\
						.format(len(chains), ", ".join(chains), self.clean_struct_fnm)
					return False
		return True

	############################################################
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


	def report_input_params(self):
		print(">>>>>>>>>>  qry name ", self.qry_name)
		print(">>>>>>>>>>  seq file name ", self.seq_file.filename if self.seq_file else "None")
		print(">>>>>>>>>>  aligned", self.aligned)
		print(">>>>>>>>>>  struct file name ", self.struct_file.filename if self.struct_file else "None")
		print(">>>>>>>>>>  chain ", self.chain)
		print(">>>>>>>>>>  method ", self.method)
		print(">>>>>>>>>>  upload folder ", Config.UPLOAD_PATH)



