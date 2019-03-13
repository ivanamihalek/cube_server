

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
