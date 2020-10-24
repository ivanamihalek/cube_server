import os, subprocess
from cube import Config


class Utils:
	def __init__(self, job_id):
		self.errmsg = None
		self.workdir   = "{}/{}".format(Config.WORK_DIRECTORY, job_id)
		self.work_path = "{}/{}".format(Config.WORK_PATH, job_id)

	def construct_afa_name(self, infile_name):
		afa_name_root = ".".join((infile_name.split("/")[-1]).split(".")[:-1])
		output_afa_name = "{}.afa".format(afa_name_root)
		return output_afa_name

	def msf2afa(self, input_msf, output_afa):
		converter = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['msf2afa'])
		cmd = "{} {}  > {}".format(converter, input_msf, output_afa)
		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if process.returncode!=0 or os.path.getsize(output_afa)==0:
			self.errmsg = "Problem converting msf to afa."
			return False
		return True

	def align(self, input_fasta, output_afa):
		muscle = Config.DEPENDENCIES['muscle']
		muscle_out = "muscle.out"
		cmd = "{} -in {} -out {} > {}".format(muscle, input_fasta, output_afa, muscle_out)
		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if process.returncode!=0:
			self.errmsg = "Problem in profile alignment"
			return False

		if os.path.getsize(output_afa)==0:
			self.errmsg = "Problem in alignment. "
			return False

		return True

	def pymol_script(self, annotation_type, pml_args):
		# having pymol is optional;
		# if we have pymol, produce pymol session, otherwise just pml script
		pymol = Config.OPTIONAL['pymol']

		[original_structure_path, method, score_file, chain, ref_seq_name] = [None]*5
		if annotation_type=="cons": # specs is conservation program - legacy naming
			[original_structure_path, method, score_file, chain] = pml_args
		elif annotation_type=="spec":
			[original_structure_path, score_file, chain, ref_seq_name] = pml_args
		if not original_structure_path: return
		# note that we will use the original structure here, with other chains, ions etc
		pdbname = original_structure_path.split("/")[-1]
		# the basic input is the specs score file
		if annotation_type=="cons": # specs is conservation program - legacy naming
			pml_creator = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['specs2pml'])
			output_name_root = "conservation_on_the_structure"
			cmd = "{} {} {} {} {}.pml {}".format(pml_creator, method, score_file, pdbname, output_name_root, chain)
		else: # annotation_type=="spec"
			pml_creator = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['hc2pml'])
			output_name_root = "specialization_on_the_structure"
			# the basic input is the specs score file
			cmd = "{} {} {} {}.pml ".format(pml_creator, score_file, pdbname, output_name_root)
			if chain: cmd += " -c {}".format(chain)
			cmd += " -g {}".format(ref_seq_name)

		if pymol:  cmd += " -p"

		process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		# are these scripts correctly returning 0 ?
		if process.returncode !=0: return None
		pml = "{}/{}.pml".format(self.workdir,output_name_root)
		pse_zip =None

		if pymol:
			os.symlink(original_structure_path, pdbname)
			cmd = "{} -qc -u  {}.pml > /dev/null ".format(pymol, output_name_root)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			os.unlink(pdbname)
			if process.returncode !=0: return None

			session = "{}.pse".format(output_name_root)
			zipfile = session+ ".zip"
			# shellzip to be distinguished from zip command in python
			shellzip = Config.DEPENDENCIES['zip']
			cmd = "{} {} {} > /dev/null ".format(shellzip, zipfile, session)
			process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			if process.returncode ==0:
				pse_zip = "{}/{}.pse.zip".format(self.workdir,output_name_root)
				os.remove(session)


		return [pml, pse_zip]



	def align_all(self, input_fastas, output_afas):
		for i in range(len(input_fastas)):
			self.align(input_fastas[i], output_afas[i])
