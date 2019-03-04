from typing import Any

from cube import Config
import subprocess,  os, shutil

# the alignment file probably needs to be checked

class Conservationist:

        def __init__(self, upload_handler):
            self.job_id = upload_handler.job_id
            self.workdir = "{}/{}".format(Config.WORK_DIRECTORY, self.job_id)
            self.work_path = "{}/{}".format(Config.WORK_PATH, self.job_id)
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
            self.preprocessed_afa = ""
            self.xls = None
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

            outf = open("%s/cmd"%self.work_path, "w")
            outf.write(prms_string)
            outf.close()
            if self.original_struct_file:
                prms_string += "pdbf      %s\n" %  self.original_struct_file
                prms_string += "pdbseq    %s\n" %  self.pdbseq
                #dssp_file  &&  (prms_string += "dssp   dssp_file\n");
                

        def prepare_run(self):
            os.mkdir(self.work_path)
            # transform msf to afa

            # if not aligned - align

            # restrict to query

            # extract sequence from pdb

            # align pdbseq to the rest of the alignment
            self.preprocessed_afa = self.original_alignment_file
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
            # the basic input is the specs score file
            xls_input =  "{}/{}.score".format(self.work_path, self.specs_outname)
            output_name_root = self.original_alignment_file.split("/")[-1].split(".")[0]
            output_path = "{}/{}".format(self.work_path, output_name_root)
            # if we have the annotation, add the annotation
            #
            xls_script = "{}/{}".format(Config.SCRIPTS_PATH, Config.SCRIPTS['specs2xls'])
            cmd = "{}   {}  {}".format(xls_script, xls_input,  output_path)
            process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            print(" ++++++ ", cmd)
            if process.returncode==0:
                self.xls = "%s.xls" % output_path

            return

        def pymol_script(self):
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

            self.run_ok = True
            return