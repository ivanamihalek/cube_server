

from cube import Config
from cube.activities.utils import Utils

import subprocess,  os
from shutil import copyfile, move

# the alignment file probably needs to be checked

class Specialist:

		def __init__(self, upload_handler):

			# directories
			self.job_id = upload_handler.job_id
			self.workdir   = "{}/{}".format(Config.WORK_DIRECTORY, self.job_id)
			self.work_path = "{}/{}".format(Config.WORK_PATH, self.job_id)

			# input
			self.original_seqfile_paths = upload_handler.original_seqfile_paths
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
			self.preprocessed_afas = []
			self.representative_seq = {}
			self.profile_afa = None
			self.xls = None
			self.pdbseq = None

			self.clean_structure_path = None
			self.pse_zip = None

			self.workdir_zip = None

			self.warn = None

			# toolbox
			self.utils = Utils(self.job_id)
			return


		##############################################
		def _group_prep(self):
			if not self.preprocessed_afas or len(self.preprocessed_afas)==0: return False
			self.group_file = "{}/groups".format(self.work_path)
			outf = open(self.group_file, "w")
			for alnmt_file in self.preprocessed_afas:
				sequence_names = []
				inf = open(alnmt_file,"r")
				for line in inf:
					if line[0] != ">": continue
					seqname = line[1:].strip().split(" ")[0]
					sequence_names.append(seqname)
					if (self.ref_seq_name and seqname==self.ref_seq_name) or alnmt_file not in self.representative_seq:
						self.representative_seq[alnmt_file]=seqname

				inf.close()
				outf.write("name "+self.representative_seq[alnmt_file] + "\n")
				outf.write("\n".join(sequence_names)+"\n")
			outf.close()
			return True

		########################
		def _profile_alnmt(self):
			prev_aln = "{}/prev.afa".format(self.work_path)
			last_aln = "{}/all.afa".format(self.work_path)
			copyfile(self.preprocessed_afas[0], last_aln)
			muscle_out = None
			for afa in self.preprocessed_afas[1:]:
				move(last_aln, prev_aln)
				muscle = Config.DEPENDENCIES['muscle']
				muscle_out = "{}/muscle.out".format(self.work_path)
				cmd = "{} -profile -in1 {} -in2 {} -out {} > {}".format(muscle, prev_aln, afa, last_aln, muscle_out)
				process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				if process.returncode!=0:
					self.warn = "Problem in profile alignment"
					self.profile_afa = None
					return False
			if os.path.getsize(last_aln)==0:
				self.warn  = "Problem in profile alignment. Are your sequences aligned?"
				self.warn += "If not please un-tick the 'My sequences are not aligned' checkbox."
				self.profile_afa = None
				return False
			self.profile_afa = last_aln
			os.remove(prev_aln)
			if muscle_out and os.path.getsize(muscle_out)==0: os.remove(muscle_out)
			return True

		########################
		def _restrict_to_qry(self):
			afa_prev = self.profile_afa
			if not self.representative_seq or len(self.representative_seq)==0: return False
			rep_seq_names = " ".join(list(self.representative_seq.values()))
			restrict_to_qry_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['restrict_afa_to_query'])
			self.preprocessed_afa = "{}/alnmt_restricted_to_ref_seq.afa".format(self.work_path)
			cmd = "{} {} {} > {}".format(restrict_to_qry_script, afa_prev, rep_seq_names, self.preprocessed_afa)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode!=0:
				self.warn = "Problem restricting to reference sequence"
				self.preprocessed_afa = afa_prev
				return False
			return True

		########################
		def _structure_prep(self):
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
					return False
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
						return False
			return True

		########################
		def _write_cmd_file(self):
			prms_string = ""

			prms_string += "patch_sim_cutoff   0.4\n"
			prms_string += "patch_min_length   0.4\n"
			prms_string += "max_gaps  0.3\n"
			prms_string += "almtname  %s\n" % self.preprocessed_afa.split("/")[-1]
			prms_string += "groups    %s\n" % self.group_file.split("/")[-1]
			prms_string += "\n"
			prms_string += "outname  %s\n" % self.specs_outname
			if self.clean_structure_path:
				prms_string += "pdb_file     %s\n" % self.clean_structure_path.split("/")[-1]
				prms_string += "pdb_name   %s\n" % self.pdbseq.split("/")[-1]
				#dssp_file  &&  (prms_string += "dssp   dssp_file\n");

			if self.method=="cube_sim":
				prms_string += "exchangeability\n"
			prms_string += "rate_matrix  %s/%s\n" % (Config.DATA_PATH, Config.DATA["tillier"])

			outf = open("%s/cmd"%self.work_path, "w")
			outf.write(prms_string)
			outf.close()

		#############################################
		def _prepare_run(self):

			# transform msf to afa

			# if not aligned - align
			self.preprocessed_afas = []
			for seqfile in self.original_seqfile_paths:
				preprocessed_afa = self.utils.construct_afa_name(seqfile)
				if self.input_aligned:
					filetype = self.seq_input_types[seqfile]
					if filetype=='fasta':
						# TODO check all seqs the same length
						copyfile(seqfile, preprocessed_afa)
					elif filetype=='gcg':
						# convert to afa
						if not self.utils.msf2afa(seqfile, preprocessed_afa):
							self.errmsg = self.utils.errmsg
							return None
						# again check if the same length
				else:
					# if not aligned - align
					if not self.utils.align(seqfile, preprocessed_afa):
						self.errmsg = self.utils.errmsg
						return None
				self.preprocessed_afas.append(preprocessed_afa)

			# group file
			# (what could go wrong here?)
			if not self._group_prep(): return

			# profile alignment for all files that we have
			if not self._profile_alnmt(): return

			# restrict the alignment to positions that
			# are not gap in at leas one of the group representatives
			self._restrict_to_qry()

			# cleanup pdb and extract chain
			if not self._structure_prep(): return

			# command file for the scoring prog
			self._write_cmd_file()


		############################################################################
		def check_run_ok(self, process):
			if process.returncode != 0:
				self.errmsg  = process.stdout
				self.errmsg += process.stderr
				self.run_ok = False
				return False
			self.score_file = "{}/{}.score".format(self.work_path, self.specs_outname)
			return True

		def specialization_map(self):
			# extract the input for the java file
			specs_score_file = "{}/{}.score".format(self.work_path, self.specs_outname)
			inf = open(specs_score_file,"r")
			png_input_file =  "{}/{}".format(self.work_path, self.png_input)
			outf = open(png_input_file,"w")
			number_of_groups = len(self.representative_seq)
			resi_count = 0
			cons_column = 2
			spec_column = cons_column + number_of_groups+1
			aa_type     = (3+2*(number_of_groups+1)) - 1
			aa_number   = aa_type + 1
			for line in inf:
				fields = line.split()
				if '%' in fields[0]: continue
				outf.write(" ".join([fields[cons_column], fields[spec_column], fields[aa_type], fields[aa_number]])+"\n")
				resi_count += 1
			inf.close()
			outf.close()

			pngmaker = Config.LIBS['seqreport-spec.jar']
			png_root = 'specialization_map'
			f_counter = resi_count//self.illustration_range+1
			for i in range(f_counter):
				seq_frm = i*self.illustration_range + 1
				seq_to  = resi_count if (i+1)*self.illustration_range > resi_count else (i+1)*self.illustration_range
				out_fnm = "{}.{}_{}" .format(png_root, seq_frm, seq_to)  # seqreport will attach the extension ".png"

				cmd  = f"java -jar  {pngmaker}  {png_input_file} {self.work_path}/{out_fnm} {seq_frm} {seq_to} "
				cmd += f"> {self.work_path}/seqreport-spec.out 2>&1"
				process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				if process.returncode==0:
					self.png_files.append(out_fnm+".png")
			return

		def excel_spreadsheet(self):
			output_name_root = "specialization_on_the_sequence"
			output_path = "{}/{}.xls".format(self.work_path, output_name_root)
			# if we have the annotation, add the annotation
			#
			xls_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['hc2xls'])
			# the basic input is the specs score file
			cmd = "{}   {}  {}".format(xls_script, self.score_file,  output_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode==0:
				self.xls = "{}/{}.xls".format(self.workdir,output_name_root)
			return

		def pymol_script(self):
			pml_args = [self.original_structure_path, self.score_file, self.chain, self.ref_seq_name ]
			ret = self.utils.pymol_script("spec", pml_args)
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
			curr = os.getcwd()
			os.chdir(self.work_path)

			### prepare
			self._prepare_run()

			### cube
			cube = "%s cmd "% Config.DEPENDENCIES['cube']
			process = subprocess.run([cube], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			### check specs finished ok
			if not self.check_run_ok(process): return

			# ### postprocess
			self.specialization_map()
			self.excel_spreadsheet()
			self.pymol_script()
			self.directory_zip()
			os.chdir(curr)

			self.run_ok = True
			return
