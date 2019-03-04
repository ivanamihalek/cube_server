import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    UPLOAD_PATH = "/tmp/cube-server"
    WORK_DIRECTORY   = "workdir"
    # set in _init_py:
    APP_PATH = None
    WORK_PATH = None
    SCRIPTS_PATH = "scripts"

    ALLOWED_SEQFILE_EXTENSIONS = {'txt', 'fasta', 'fst', 'fa', 'gcg', 'msf', 'afa'}
    ALLOWED_STRUCTFILE_EXTENSIONS = {'pdb'}

    DEPENDENCIES = {'specs': '/var/local/bin/specs',
                    'muscle':'/var/local/bin/muscle',
                    'mafft':'/var/local/bin/mafft/mafft.sh'  # https://mafft.cbrc.jp/alignment/software/linuxportable.html
                    }
    LIBS = {'seqreport.jar': '/var/local/java/SeqReport.jar',
                    'seqreport-spec.jar': '/var/local/java/SeqReportEE.jar'
            }

    SCRIPTS = {"afa2msf":"afa2msf.pl", "docx2txt":"docx2txt.pl",
               "fasta_rename_seqs":"fasta_rename_seqs.pl", "hc2chimera":"hc2chimera.pl",
               "hc2pml":"hc2pml.pl", "hc2xls":"hc2xls.pl", "msf2afa":"msf2afa.pl",
               "pdb2seq":"pdb2seq.pl", "pdb_extract_chain_and_cleanup":"pdb_extract_chain_and_cleanup.pl",
               "restrict_msf_to_query":"restrict_msf_to_query.pl",
               "sort_by_taxonomy":"sort_by_taxonomy.pl", "specs2pml":"specs2pml.pl", "specs2xls":"specs2xls.pl"}

    PERL_MODULES = ['Spreadsheet::WriteExcel']