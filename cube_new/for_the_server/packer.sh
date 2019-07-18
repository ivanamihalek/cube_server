tar -cvf current.tar cube/ requirements.txt cube.wsgi run.py
gzip current.tar
source ~/.bashrc
to_dogmatic current.tar.gz && rm -f current.tar.gz

