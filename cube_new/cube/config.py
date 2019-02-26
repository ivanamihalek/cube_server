import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    UPLOAD_DIRECTORY = '/tmp/cube-server'
    WORK_DIRECTORY = "workdir"
    ALLOWED_SEQFILE_EXTENSIONS = {'txt', 'fasta', 'fst', 'fa', 'gcg', 'msf', 'afa'}
    ALLOWED_STRUCTFILE_EXTENSIONS = {'pdb'}

    DEPENDENCIES = {'specs':'/var/local/bin/specs',
                    'muscle':'/var/local/bin/muscle',
                    'mafft':'/var/local/bin/mafft/mafft.sh', # https://mafft.cbrc.jp/alignment/software/linuxportable.html
                    }
