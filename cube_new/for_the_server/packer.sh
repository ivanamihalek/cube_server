tar -cvf current.tar cube/ requirements.txt cube.wsgi
source ~/.bashrc
to_mono current.tar && rm -f current.tar
