tar -cvf current.tar cube/ requirements.txt cube.wsgi
gzip current.tar
source ~/.bashrc
to_mono current.tar.gz && rm -f current.tar.gz

