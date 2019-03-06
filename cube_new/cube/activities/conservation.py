from typing import Any

from cube import Config
import subprocess,  os, shutil

# the alignment file probably needs to be checked

class Conservationist:

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
			return

		def _write_cmd_file(self):
			prms_string = ""
			prms_string += "patch_sim_cutoff   0.4\n"
			prms_string += "patch_min_length   0.4\n"
			prms_string += "sink  0.3  \n"
			prms_string += "skip_query \n"
			prms_string += "\n"

			prms_string += "align   %s\n" % self.preprocessed_afa
			prms_string += "refseq  %s\n" % self.qry_name
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
			os.mkdir(self.work_path)
			# transform msf to afa

			# if not aligned - align

			# restrict to query

			# cleanup pdb and extract chain
			# (note that it will also produce file with the corresponding sequence)
			pdb_cleanup_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['pdb_cleanup'])
			self.pdbseq = ".".join(self.original_structure_path.split("/")[-1].split(".")[:-1])+self.chain
			cmd = "{} {} {} {} {}".format(pdb_cleanup_script, self.original_structure_path,
									self.pdbseq, self.chain, self.work_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode!=0:
				self.original_structure_path = None
				return
			self.clean_structure_path = "{}/{}.pdb".format(self.work_path, self.pdbseq)
			# HERE !!!
			# align pdbseq to the rest of the alignment
			self.preprocessed_afa = self.original_alignment_path
			self._write_cmd_file()

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
			output_name_root = "conservation_on_the_sequence"
			output_path = "{}/{}".format(self.work_path, output_name_root)
			# if we have the annotation, add the annotation
			#
			xls_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['specs2xls'])
			# the basic input is the specs score file
			cmd = "{}   {}  {}".format(xls_script, self.score_file,  output_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode==0:
				self.xls = "%s.xls" % output_path

			return

		def pymol_script(self):
			if not self.original_structure_path: return
			output_name_root = "conservation_on_the_structure"
			output_path = "{}/{}".format(self.work_path, output_name_root)
			#cmd = "$specs2pml  $score_method  $score_f  $structure $script "
			#($chainID_in_pdb_file =~ / \w /) & & ($cmd.= " $chainID");
			pml_creator = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['specs2pml'])
			# the basic input is the specs score file
			cmd = "{}   {}  {}".format(pml_creator, self.score_file,  output_path)
			print(" ++++++ ", cmd)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			# are these scripts correctly returning 0 ?
			if process.returncode !=0: return

			pymol = Config.DEPENDENCIES['pymol']
			cmd = "{} -qc -u  {} > /dev/null ".format(pymol, output_path)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode !=0: return


			session = "{}/{}.pse".format(self.work_path, output_name_root)
			zipfile = session+ ".zip"
			# shellzip to be distinguished from zip command in python
			shellzip =  Config.DEPENDENCIES['zip']
			cmd = "{} -i {} {} > /dev/null ".format(shellzip,zipfile, session )
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode !=0: return

			return

		def directory_zip(self):
			return

		###################################################
		def run(self):

			### prepare
			self.prepare_run()

			### specs
			specs = Config.DEPENDENCIES['specs']
			cmd = "{} {}/cmd ".format(specs, self.work_path)
			print(" +++ ", cmd)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			### check specs finshed ok
			if not self.check_run_ok(process): return

			### postprocess
			self.conservation_map()
			self.excel_spreadsheet()
			self.pymol_script()

			self.run_ok = True
			return
