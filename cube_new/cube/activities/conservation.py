from typing import Any

from cube import Config
import subprocess,  os, shutil

# the alignment file probably needs to be checked

class Conservationist:

        def __init__(self, upload_handler):
            self.job_id = upload_handler.job_id
            self.static_path =  "{}/{}".format(Config.WORK_DIRECTORY, self.job_id)
            self.workdir = "{}/static/{}".format(Config.APP_PATH,self.static_path)
            self.original_alignment_file = "{}/{}".format(upload_handler.staging_dir, upload_handler.clean_seq_fnm)
            self.original_struct_file = None
            if upload_handler.clean_struct_fnm:
                self.original_struct_file = "{}/{}".format(upload_handler.staging_dir, upload_handler.clean_struct_fnm)
            self.qry_name = upload_handler.qry_name
            self.method = upload_handler.method
            self.specs_outname = "specs_out"
            self.png_input = "png_in"
            self.illustration_range = 400
            self.run_ok = False
            self.errmsg = None
            self.png_files = []
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
            prms_string += "outn  %s/%s\n" % (self.workdir, self.specs_outname)

            outf = open("%s/cmd"%self.workdir, "w")
            outf.write(prms_string)
            outf.close()
            if self.original_struct_file:
                prms_string += "pdbf      %s\n" %  self.original_struct_file
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

            self.prepare_run()

            ### specs
            specs = Config.DEPENDENCIES['specs']
            cmd = "{} {}/cmd ".format(specs, self.workdir)
            print(" +++ ", cmd)
            process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if process.returncode != 0:
                self.errmsg  = process.stdout
                self.errmsg += process.stderr
                self.run_ok = False
                return

            ### cins map
            # extract the input for the java file
            specs_score_file = "{}/{}.score".format(self.workdir, self.specs_outname)
            inf = open(specs_score_file,"r")
            png_input_file =  "{}/{}".format(self.workdir, self.png_input)
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
            png_root = self.job_id
            f_counter = int(resi_count/self.illustration_range)
            for i in range(f_counter):
                    seq_frm = i*self.illustration_range + 1
                    seq_to =  resi_count if (i+1)*self.illustration_range > resi_count else (i+1)*self.illustration_range
                    out_fnm = "{}.{}_{}" .format(png_root, seq_frm, seq_to)
                    cmd = "java -jar  {}  {}  {} {} {} > {}/seqReport.out 2>&1".\
                        format(pngmaker, png_input_file, "{}/{}".format(self.workdir, out_fnm), seq_frm, seq_to, self.workdir)
                    process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    if process.returncode==0:
                        self.png_files.append(out_fnm+".png")

            self.run_ok = True
            return