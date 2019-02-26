from typing import Any

from cube import Config
import subprocess, os, shutil

# the alignment file probably needs to be checked

class Conservationist:

        def __init__(self, uploadHandler):
            self.job_id = uploadHandler.job_id
            self.workdir = "{}/{}".format(Config.WORK_DIRECTORY, self.job_id)
            self.original_alignment_file = "{}/{}".format(uploadHandler.staging_dir, uploadHandler.clean_seq_fnm)
            self.original_struct_file = None
            if uploadHandler.clean_struct_fnm:
                self.original_struct_file = "{}/{}".format(uploadHandler.staging_dir, uploadHandler.clean_struct_fnm)
            self.qry_name = uploadHandler.qry_name
            self.method = uploadHandler.method
            self.run_ok = False
            return

        def _write_cmd_file(self):
            prms_string = ""
            prms_string += "patch_sim_cutoff   0.4\n"
            prms_string += "patch_min_length   0.4\n"
            prms_string += "sink  0.3  \n"
            prms_string += "skip_query \n"
            prms_string += "\n"
         
            prms_string += "align   %s\n" % self.original_alignment_file
            prms_string += "refseq  %s\n" % self.qry_name
            prms_string += "method  %s\n" % self.method
            prms_string += "\n";
            prms_string += "outn  %s/specs_out\n" % self.workdir

            outf = open("%s/cmd"%self.workdir, "w")
            outf.write(prms_string)
            outf.close()
            if self.original_struct_file:
                prms_string += "pdbf      %s\n" %  self.original_strut_file
                prms_string += "pdbseq    %s\n" %  self.pdbseq
                #dssp_file  &&  (prms_string += "dssp   dssp_file\n");
                

        def prepare_run(self):
            os.mkdir(self.workdir)
            self._write_cmd_file()
            # transform msf to afa

            # if not aligned - align

            # restrict to query

            # extract sequence from pdb

            # align pdbseq to the rest of the alignment


        def run(self):
            specs = Config.DEPENDENCIES['specs']
            cmd = "{} {}/cmd ".format(specs, self.workdir)
            print(" +++ ", cmd)
            process = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True)
            self.run_ok = True
            return