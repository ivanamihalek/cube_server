

from cube import Config
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
			self.original_alignment_paths = upload_handler.original_alignment_paths
			self.original_structure_path = upload_handler.original_structure_path
			self.chain = upload_handler.chain if upload_handler.chain else "-"
			self.ref_seq_name = upload_handler.ref_seq_name

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
				self.warn = "Problem in profile alignment. Are your sequences aligned?"
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
			if self.ref_seq_name:
				restrict_to_qry_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['restrict_afa_to_query'])
				self.preprocessed_afa = "{}/alnmt_restricted_to_ref_seq.afa".format(self.work_path)
				cmd = "{} {} {} > {}".format(restrict_to_qry_script, afa_prev, self.ref_seq_name, self.preprocessed_afa)
				process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				if process.returncode!=0:
					self.warn = "Problem restricting to reference sequence"
					self.profile_afa = afa_prev
			return True


		########################
		def _structure_prep(self):
			afa_prev = self.profile_afa
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
					self.profile_afa = "{}/alnmt_w_pdb_seq.afa".format(self.work_path)
					cmd = "{} --add {} {} > {}".format(mafft, self.clean_structure_path.replace('.pdb', '.seq'), afa_prev, self.profile_afa)
					process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
					if process.returncode!=0:
						self.profile_afa = afa_prev
						self.warn = "Problem running mafft"
						self.original_structure_path = None
						return False
			return True

		########################
		def _group_prep(self):
			for alnmt_file in self.preprocessed_afas:
				inf = open(alnmt_file,"r")
				for line in inf:
					if line[0] != ">": continue
					seqname = line[1:].strip().split(" ")[0]
					if (self.ref_seq_name and seqname == self.ref_seq_name) or alnmt_file not in self.representative_seq:
						self.representative_seq[alnmt_file]=seqname
				inf.close()
			return

		###################################################
		def _prepare_run(self):
			os.mkdir(self.work_path)
			# transform msf to afa

			# if not aligned - align
			# TODO this might not exist if we are aligning ourselves
			self.preprocessed_afas = self.original_alignment_paths

			# group file
			if not self._group_prep(): return

			# profile alignment for all files that we have
			if not self._profile_alnmt(): return
			return

			# restrict the alignmen to positions that
			# are not gap in at leas one of the group representatives
			self._restrict_to_qry()
			return

			# cleanup pdb and extract chain
			if not self._structure_prep(): return

			# command file for the scoring prog
			self._write_cmd_file()




			self._write_cmd_file()
		################
		def check_run_ok(self, process):
			if process.returncode != 0:
				self.errmsg  = process.stdout
				self.errmsg += process.stderr
				self.run_ok = False
				return False
			if "Unrecognized amino acid code" in process.stdout.decode("utf-8"):
				self.errmsg  = process.stdout
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
			f_counter = int(resi_count/self.illustration_range)
			for i in range(f_counter):
				seq_frm = i*self.illustration_range + 1
				seq_to =  resi_count if (i+1)*self.illustration_range > resi_count else (i+1)*self.illustration_range
				out_fnm = "{}.{}_{}" .format(png_root, seq_frm, seq_to)
				cmd = "java -jar  {}  {}  {} {} {} > {}/seqReport.out 2>&1". \
					format(pngmaker, png_input_file, "{}/{}".format(self.work_path, out_fnm), seq_frm, seq_to, self.work_path)
				process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				if process.returncode==0:
					self.png_files.append(out_fnm+".png")
			return

		def excel_spreadsheet(self):
			output_name_root = "specialization_on_the_sequence"
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
			# note that we will use the original structure here, with other chains, ions etc
			if not self.original_structure_path: return
			output_name_root = "specialization_on_the_structure"
			output_path = "{}/{}".format(self.work_path, output_name_root)
			pml_creator = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['specs2pml'])
			# the basic input is the specs score file
			cmd = "{} rvet {} {} {}.pml {}".format(pml_creator, self.score_file, self.original_structure_path, output_path, self.chain)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			# are these scripts correctly returning 0 ?
			if process.returncode !=0: return

			pymol = Config.DEPENDENCIES['pymol']
			cmd = "{} -qc -u  {}.pml > /dev/null ".format(pymol, output_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode !=0: return

			session = "{}.pse".format(output_path)
			zipfile = session+ ".zip"
			# shellzip to be distinguished from zip command in python
			shellzip = Config.DEPENDENCIES['zip']
			cmd = "{} {} {} > /dev/null ".format(shellzip, zipfile, session)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode ==0:
				self.pse_zip = "{}/{}.pse.zip".format(self.workdir,output_name_root)

			return

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

			### prepare
			self._prepare_run()

			### cube
			# cube = Config.DEPENDENCIES['cube']
			# cmd = "{} {}/cmd ".format(cube, self.work_path)
			# print(" +++ ", cmd)
			# process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			### check specs finished ok
			# if not self.check_run_ok(process): return
			#
			# ### postprocess
			# self.specialization_map()
			# self.excel_spreadsheet()
			# self.pymol_script()
			# self.directory_zip()

			self.run_ok = True
			return
