import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    UPLOAD_DIRECTORY = '/tmp/cube-server'
    WORK_DIRECTORY = "workdir"
    APP_PATH = None # set in _init_py
    ALLOWED_SEQFILE_EXTENSIONS = {'txt', 'fasta', 'fst', 'fa', 'gcg', 'msf', 'afa'}
    ALLOWED_STRUCTFILE_EXTENSIONS = {'pdb'}

    DEPENDENCIES = {'specs': '/var/local/bin/specs',
                    'muscle':'/var/local/bin/muscle',
                    'mafft':'/var/local/bin/mafft/mafft.sh'  # https://mafft.cbrc.jp/alignment/software/linuxportable.html
                    }
    LIBS = {'seqreport.jar': '/var/local/java/SeqReport.jar',
                    'seqreport-spec.jar': '/var/local/java/SeqReportEE.jar'
            }

