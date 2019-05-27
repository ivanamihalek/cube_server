

from cube import Config
import subprocess,  os, shutil

# the alignment file probably needs to be checked

class Specializer:

		def __init__(self, upload_handler):

			# directories
			self.job_id = upload_handler.job_id
			self.workdir = "{}/{}".format(Config.WORK_DIRECTORY, self.job_id)
			self.work_path = "{}/{}".format(Config.WORK_PATH, self.job_id)

			# input
			self.original_alignment_path = upload_handler.original_alignment_path
			self.original_structure_path = upload_handler.original_structure_path
			self.chain = upload_handler.chain if upload_handler.chain else "-"
			self.qry_name = upload_handler.qry_name

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

			self.workdir_zip = None

			self.warn = None
			return


		def _write_cmd_file(self):
			prms_string = ""
			prms_string += "patch_sim_cutoff   0.4\n"
			prms_string += "patch_min_length   0.4\n"
			prms_string += "sink  0.3  \n"
			prms_string += "skip_query \n"
			prms_string += "\n"

			prms_string += "align   %s\n" % self.preprocessed_afa
			prms_string += "groups  %s\n" % self.group_file

			prms_string += "\n"
			prms_string += "outn  %s/%s\n" % (self.work_path, self.specs_outname)
			if self.clean_structure_path:
				prms_string += "pdbf      %s\n" % self.clean_structure_path
				prms_string += "pdbseq    %s\n" % self.pdbseq
				#dssp_file  &&  (prms_string += "dssp   dssp_file\n");

			outf = open("%s/cmd"%self.work_path, "w")
			outf.write(prms_string)
			outf.close()



		def prepare_run(self):
			os.mkdir(self.work_path)
			# transform msf to afa

			# if not aligned - align
			# TODO this might not exist if we are aligning ourselves
			self.preprocessed_afa = self.original_alignment_path

			# restrict to query
			afa_prev = self.preprocessed_afa
			if self.qry_name:
				restrict_to_qry_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['restrict_afa_to_query'])
				self.preprocessed_afa = "{}/alnmt_restricted_to_ref_seq.afa".format(self.work_path)
				cmd = "{} {} {} > {}".format(restrict_to_qry_script, afa_prev, self.qry_name, self.preprocessed_afa)
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
						return
			self._write_cmd_file()


		###################################################
		def run(self):

			### prepare
			self.prepare_run()

			### cube
			cube = Config.DEPENDENCIES['cube']
			cmd = "{} {}/cmd ".format(cube, self.work_path)
			print(" +++ ", cmd)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			### check specs finished ok
			if not self.check_run_ok(process): return

			### postprocess
			self.conservation_map()
			self.excel_spreadsheet()
			self.pymol_script()
			self.directory_zip()

			self.run_ok = True
			return
