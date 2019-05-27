
from werkzeug.utils import secure_filename
from cube.config import Config
import os, subprocess
import string, random

class UploadHandler:
	def __init__(self, request, multiple_seq_files=False):
		self.multiple_seq_files = multiple_seq_files
		self.qry_name    = request.form['qry_nm']
		if multiple_seq_files:
			# careful:  request.files is empty dict if no file selected
			self.seq_files = request.files.getlist('fnms') if 'fnm' in request.files else None
		else:
			self.seq_files = [request.files['fnm']] if 'fnm' in request.files else None

		self.original_alignment_paths = []
		self.original_alignment_path  = None
		# ditto for the checkbox   - if not checked, it does not exist
		self.aligned     = ('aligned' in  request.form)

		self.clean_seq_fnms = {}
		# this will be the copy of the first file name - so I can recycle the code for both spec and conservation
		# (conservation takes only one sequence file)
		self.clean_seq_fnm = None
		self.seq_input_types = {}
		self.seq_input_type = None

		########################################
		self.struct_file = request.files['structure_fnm'] if 'structure_fnm' in request.files else None
		self.original_structure_path = None
		self.chain       = request.form['chain']
		self.method      = request.form['method']
		self.clean_struct_fnm = None

		########################################
		self.job_id = self._id_generator()
		self.staging_dir = "{}/{}".format(Config.UPLOAD_PATH, self.job_id)
		self.errmsg = None

	def _id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	def _allowed_file(self, filename, allowed_extensions):
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

	############################################################
	#
	def _find_seq_input_type(self, alignment_path):
		cmd = "grep  '>' {} ".format(alignment_path)
		output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
		if len(output)>0:
			self.seq_input_type = 'fasta'
			return 'fasta'
		cmd = "grep  'Name: ' {} ".format(alignment_path)
		output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
		if len(output)>0:
			self.seq_input_type = 'gcg'
			return 'gcg'
		return None

	def _ref_seq_ok(self):
		refseq_ok = False
		for alignment_path in self.original_alignment_paths:
			if self.seq_input_types[alignment_path] == 'fasta':
				cmd = "grep  '>' {} | grep {}".format(alignment_path, self.qry_name)
			else:
				cmd = "grep 'Name: '  {} | grep {} ".format(alignment_path, self.qry_name)
			output = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True).stdout
			if len(output)>0:
				refseq_ok = True
				break
		return refseq_ok

	############################################################
	#
	def upload_files(self):
		os.makedirs(self.staging_dir, exist_ok=True)
		for seq_file, clean_seq_fnm in self.clean_seq_fnms.items():
			print ("************* saving", clean_seq_fnm)
			self.original_alignment_paths.append(os.path.join(self.staging_dir, clean_seq_fnm))
			seq_file.save(self.original_alignment_path)
		if not self.multiple_seq_files: self.original_alignment_path = self.original_alignment_paths[0]
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
		for alignment_path in self.original_alignment_paths:
			seq_input_type = self._find_seq_input_type(alignment_path)
			if not seq_input_type:
				self.errmsg = "Sequence file format not recognized."
				return False
			self.seq_input_types[alignment_path] = seq_input_type
		if not self.multiple_seq_files: self.seq_input_type= self.seq_input_types.values()[0]
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
		if self.multiple_seq_files:
			if not self.seq_files or len(self.seq_files)<2 \
					or self.seq_files[0].filename == '' or self.seq_files[1]== '':
				self.errmsg = "Please provide at least 2 files with input sequences."
				return False
		else:
			if not self.seq_files or len(self.seq_files)<1 or self.seq_files[0].filename == '':
				self.errmsg = "Please provide a file with input sequences."
				return False
		for seq_file in self.seq_files:
			clean_seqname = secure_filename(seq_file.filename)
			if not clean_seqname or clean_seqname == '':
				if self.multiple_seq_files:
					self.errmsg = "Please provide input sequences in files with reasonable names."
				else:
					self.errmsg = "Please provide input sequences in a file with reasonable name."
				return False
			if not self._allowed_file(clean_seqname, Config.ALLOWED_SEQFILE_EXTENSIONS):
				if self.multiple_seq_files:
					self.errmsg = "Please provide input sequences in files with with one of the extensions: "
				else:
					self.errmsg = "Please provide input sequences in a file with one of the extensions: "
				self.errmsg += ", ".join([e for e in Config.ALLOWED_SEQFILE_EXTENSIONS])
				return False
			self.clean_seq_fnms[seq_file] = clean_seqname
		if not self.multiple_seq_files: self.clean_seq_fnm = self.clean_seq_fnms.values()[0]
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
		if self.seq_files:
			for fnm in self.seq_file.filenames:
				print(">>>>>>>>>>  seq file name ", fnm)
		print(">>>>>>>>>>  aligned", self.aligned)
		print(">>>>>>>>>>  struct file name ", self.struct_file.filename if self.struct_file else "None")
		print(">>>>>>>>>>  chain ", self.chain)
		print(">>>>>>>>>>  method ", self.method)
		print(">>>>>>>>>>  upload folder ", Config.UPLOAD_PATH)



