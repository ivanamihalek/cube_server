
from cube import Config
from cube.activities.utils import Utils

import subprocess,  os
from shutil import copyfile

# the alignment file probably needs to be checked


class Conservationist:

	def __init__(self, upload_handler):

		# directories
		self.job_id = upload_handler.job_id
		self.workdir   = "{}/{}".format(Config.WORK_DIRECTORY, self.job_id)
		self.work_path = "{}/{}".format(Config.WORK_PATH, self.job_id)

		# input
		self.original_seqfile_path = upload_handler.original_seqfile_path
		self.seq_input_types = upload_handler.seq_input_types
		self.input_aligned = upload_handler.aligned
		self.original_structure_path = upload_handler.original_structure_path
		self.chain = upload_handler.chain if upload_handler.chain else "-"
		self.ref_seq_name = upload_handler.ref_seq_name
		self.method = upload_handler.method

		# output
		self.specs_outname = "specs_out"
		self.png_input = "png_in"
		self.illustration_range = 400
		self.run_ok = False
		self.errmsg = None
		self.score_file = None
		self.png_files = []
		self.preprocessed_afa = ""
		self.xls = None
		self.pdbseq = None

		self.clean_structure_path = None
		self.pse_zip = None
		self.pml = None

		self.workdir_zip = None
		self.warn = None

		# toolbox
		self.utils = Utils(self.job_id)
		return

	def _write_cmd_file(self):
		prms_string = ""
		prms_string += "patch_sim_cutoff   0.4\n"
		prms_string += "patch_min_length   0.4\n"
		prms_string += "sink  0.3  \n"
		prms_string += "skip_query \n"
		prms_string += "\n"

		prms_string += "align   %s\n" % self.preprocessed_afa
		prms_string += "refseq  %s\n" % self.ref_seq_name
		prms_string += "method  %s\n" % self.method
		prms_string += "\n";
		prms_string += "outn  %s/%s\n" % (self.work_path, self.specs_outname)
		if self.clean_structure_path:
			prms_string += "pdbf      %s\n" %  self.clean_structure_path
			prms_string += "pdbseq    %s\n" %  self.pdbseq
		#dssp_file  &&  (prms_string += "dssp   dssp_file\n");

		outf = open("%s/cmd"%self.work_path, "w")
		outf.write(prms_string)
		outf.close()

	def prepare_run(self):
		self.preprocessed_afa = self.utils.construct_afa_name(self.original_seqfile_path)
		if self.input_aligned:
			filetype = self.seq_input_types[self.original_seqfile_path]
			if filetype=='fasta':
				# TODO check all seqs the same length
				copyfile(self.original_seqfile_path, self.preprocessed_afa)
			elif filetype=='gcg':
				# convert to afa
				if not self.utils.msf2afa(self.original_seqfile_path, self.preprocessed_afa):
					self.errmsg = self.utils.errmsg
					return None
				# again check if the same length
		else:
			# if not aligned - align
			if not self.utils.align(self.original_seqfile_path, self.preprocessed_afa):
				self.errmsg = self.utils.errmsg
				return None

		# choose reference sequence if we do not have one
		if not self.ref_seq_name:
			cmd = "grep '>'  {} | head -n1".format(self.preprocessed_afa)
			output = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True).stdout
			self.ref_seq_name = output[1:].decode('utf8').strip().split(" ")[0]
		# restrict to query
		afa_prev = self.preprocessed_afa
		restrict_to_qry_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['restrict_afa_to_query'])
		self.preprocessed_afa = "{}/alnmt_restricted_to_ref_seq.afa".format(self.work_path)
		cmd = "{} {} {} > {}".format(restrict_to_qry_script, afa_prev, self.ref_seq_name, self.preprocessed_afa)
		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if process.returncode!=0:
			self.warn = "Problem restricting to reference sequence"
			self.preprocessed_afa = afa_prev

		# cleanup pdb and extract chain
		afa_prev = self.preprocessed_afa
		if self.original_structure_path:
			# (note that it will also produce file with the corresponding sequence)
			pdb_cleanup_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['pdb_cleanup'])
			self.pdbseq = ".".join(self.original_structure_path.split("/")[-1].split(".")[:-1])+self.chain
			cmd = "{} {} {} {} {}".format(pdb_cleanup_script, self.original_structure_path,
											self.pdbseq, self.chain, self.work_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode!=0:
				self.original_structure_path = None
				self.warn = "Problem with the structure file"
			else:
				self.clean_structure_path = "{}/{}.pdb".format(self.work_path, self.pdbseq)
				# align pdbseq to the rest of the alignment
				mafft = Config.DEPENDENCIES['mafft']
				self.preprocessed_afa = "{}/alnmt_w_pdb_seq.afa".format(self.work_path)
				cmd = "{} --add {} {} > {}".format(mafft, self.clean_structure_path.replace('.pdb', '.seq'), afa_prev, self.preprocessed_afa)
				process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				if process.returncode!=0:
					self.preprocessed_afa = afa_prev
					self.warn = "Problem running mafft"
					self.original_structure_path = None
					return None
		self._write_cmd_file()
		return True

	def check_run_ok(self, process):
		if process.returncode != 0:
			self.errmsg  = process.stdout.decode("utf-8").strip()
			self.errmsg += process.stderr.decode("utf-8").strip()
			self.run_ok = False
			return False
		if "Unrecognized amino acid code" in process.stdout.decode("utf-8"):
			self.errmsg = process.stdout.decode("utf-8")
			self.run_ok = False
			return False
		self.score_file = "{}/{}.score".format(self.work_path, self.specs_outname)
		return True

	def conservation_map(self):
		# extract the input for the java file
		specs_score_file = "{}/{}.score".format(self.work_path, self.specs_outname)
		inf = open(specs_score_file,"r")
		png_input_file =  "{}/{}".format(self.work_path, self.png_input)
		outf = open(png_input_file,"w")
		resi_count = 0
		for line in inf:
			fields = line.split()
			if '%' in fields[0] or '.' in fields[3]: continue
			outf.write(" ".join([fields[2], fields[3], fields[4]])+"\n")
			resi_count += 1
		inf.close()
		outf.close()

		pngmaker = Config.LIBS['seqreport.jar']
		png_root = 'conservation_map'
		for i in range(0,resi_count, self.illustration_range):
			seq_frm = i+1
			seq_to  = min(resi_count, i+self.illustration_range)
			out_fnm = "{}.{}_{}" .format(png_root, seq_frm, seq_to)
			cmd  = f"java -jar  {pngmaker}  {png_input_file} {self.work_path}/{out_fnm} {seq_frm} {seq_to} "
			cmd += f" > {self.work_path}/seqreport.out 2>&1"
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode==0:
				self.png_files.append(out_fnm+".png")
		return

	def excel_spreadsheet(self):
		output_name_root = "conservation_on_the_sequence"
		output_path = "{}/{}".format(self.work_path, output_name_root)
		# if we have the annotation, add the annotation
		#
		xls_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['specs2xls'])
		# the basic input is the specs score file
		cmd = "{}   {}  {}".format(xls_script, self.score_file,  output_path)
		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if process.returncode==0:
			self.xls = "{}/{}.xls".format(self.workdir,output_name_root)

		return

	def pymol_script(self):
		pml_args = [self.original_structure_path, self.method, self.score_file, self.chain]
		ret = self.utils.pymol_script("cons", pml_args)
		if ret: [self.pml, self.pse_zip] = ret

	def directory_zip(self):
		curr = os.getcwd()
		os.chdir(Config.WORK_PATH)
		shellzip = Config.DEPENDENCIES['zip']
		archive_name = "cube_workdir_{}.zip".format(self.job_id)
		cmd = "{} -r {} {} > /dev/null ".format(shellzip, archive_name, self.job_id)
		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if process.returncode ==0:
			os.rename(archive_name, "{}/{}".format(self.work_path, archive_name))
			self.workdir_zip = "{}/{}".format(self.workdir, archive_name)

		os.chdir(curr)
		return

	###################################################
	def run(self):
		os.mkdir(self.work_path)

		### from this point on we are in the workdir
		currpath = os.getcwd()
		os.chdir(self.work_path)

		### prepare
		if not self.prepare_run(): return

		### specs
		specs = Config.DEPENDENCIES['specs']
		cmd = "{} {}/cmd ".format(specs, self.work_path)
		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		### check specs finshed ok
		if not self.check_run_ok(process): return

		### postprocess
		self.conservation_map()
		self.excel_spreadsheet()
		self.pymol_script()
		self.directory_zip()

		self.run_ok = True
		return
