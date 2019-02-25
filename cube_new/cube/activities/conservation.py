from typing import Any

from cube import Config
import subprocess, os, shutil

# the alignment file probably needs to be checked

class Conservationist:

        def __init__(self, uploadHandler):
            self.id_string = uploadHandler.id_string
            self.workdir = "{}/{}".format(Config.WORK_DIRECTORY, self.id_string)
            self.alignment_file = "{}/{}/{}".format(Config.UPLOAD_DIRECTORY, self.id_string, uploadHandler.clean_seq_fnm)
            self.qry_name = uploadHandler.qry_name
            self.method = uploadHandler.method
            return

        def _write_cmd_file(self):
            prms_string = ""
            prms_string += "patch_sim_cutoff   0.4\n"
            prms_string += "patch_min_length   0.4\n"
            prms_string += "sink  0.3  \n"
            prms_string += "skip_query \n"
            prms_string += "\n"
         
            prms_string += "align   %s\n" % self.alignment_file
            prms_string += "refseq  %s\n" % self.qry_name
            prms_string += "method  %s\n" % self.method
            prms_string += "\n";
            prms_string += "outn  %s/specs_out\n" % self.workdir
        

            outf = open("%s/cmd"%self.workdir, "w")
            outf.write(prms_string)
            outf.close()
            #if structure:
            #    prms_string += "pdbf      jobdir/structure_single_chain.pdb  \n";
            #    prms_string += "pdbseq    pdb_structure_single_chain\n";
            #    #dssp_file  &&  (prms_string += "dssp   dssp_file\n");
                


        def run(self):
            specs = Config.DEPENDENCIES['specs']
            os.mkdir(self.workdir)
            self._write_cmd_file()
            cmd = "{} {}/cmd ".format(specs, self.workdir)
            print(" +++ ", cmd)
            process = subprocess.run([cmd],  stdout=subprocess.PIPE, shell=True)
