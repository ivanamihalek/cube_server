Migrating the server

==========================================================
1) COMPILING SPECS AND HYPERCUBE

Specs and hypercube can be placed in the src directory, but this is optional.
They can be found at  git://github.com/ivanamihalek/specs 
and git://github.com/ivanamihalek/hypercube respectively.

Clone to whichever directory you find handy, and compile by moving to 10_objects
and typing make. That should work in both cases. Move the produced binaries to
bin directory of the server.

In particular, make sure that src/hypercube/08_data/tillier.table exists,
and that the full path to is is given in cmd_template_cub, as
rate_matrix  $PATH_TO_SPECS_SERVER/src/hypercube/08_data/tillier.table

==========================================================
2) COMPILING JAVA PIECES

In java dir:
mkdir seqreport
cp SeqReport.java seqreport/
cd seqreport/
javac SeqReport.java
cd ..
jar cvfe SeqReport.jar seqreport.SeqReport seqreport
rm -rf seqreport

(Alternatively, you can just let NetBeans or Eclipse to this for you)

Repeat for SeqReportEE.

Move the jarfiles to (this server's) bin directory.

==========================================================
3) MUSCLE AND DSSP

Obtain a copy of Muscle and DSSP program for your platform, and place in bin.
http://www.drive5.com/muscle/
http://swift.cmbi.ru.nl/gv/dssp/
Unfortunatley, the lates version of DSSP rewuires boost, which you might also 
have to compile if you do not see it on your machine. Alternatively, 
look for a pre-compiled binary for your platform.
Hints for compileing on mac:
* run make once, it will produce make.config
* in make config cnage the boost paths
BOOST_LIB_DIR    = /usr/local/lib
BOOST_INC_DIR    = /usr/local/include/boost
but leave the -mt flag commented
* in makefile, change DEST_DIR to ./, and change  -static to  -static-intel in 
mkdssp section
* dssp is called mkdssp, for some reason

==========================================================
4) OTHER DEPENDENCIES

On several places we use perl's system() command, with  the underlying assumption
that it will invoke bash shell for controlled stdout/stderr redirection.

THe following programs are expected to be installed on the computer the server 
will be running on: mafft, pymol  and zip. See the next section about fixing
the paths to each one of them. The reason mafft is included here and not 
in the bin directory has to do eith the mafft setup itself. See here 
for the case of Mac: http://mafft.cbrc.jp/alignment/software/macosx.html.

Perl needs Spreadsheet::ParseExcel and SpreadSHeet::WriteExcel modules module.
Here are instructions fro WriteExcel. Work for ParseExcel too.
http://cpansearch.perl.org/src/JMCNAMARA/Spreadsheet-WriteExcel-2.37/docs/WriteExcel_Install.html

As it goes, these two modules depend on Crypt-RC4 and Digest-Perl-MD5, so the process
has to be repeated for them too.

==========================================================
5) FIXING THE PATHS

== In cgi-bin/specs.cgi ==

On the top of the file cgi-bin/specs.cgi, change the paths corresponding to 
$dir and $scratchdir to reflect your local setup.

Adjust the paths to the third party programs: $mafft, $pymol and $zip. You can
add a chunk of code corresponding to your $host, defined at the top of the file.

==========================================================
6) FIXING THE HTML ADDRESSES

== In cgi-bin/specs_html.pm and  cgi-bin/specs_input.pm ==

Change $homepage varaible to reflect your setup, for example
my $homepage = "eopsf.org/cube";
or
my $homepage = "cube.local";

== In www/  ==

If you really want to claim the server as yours, replace the reference to eopsf.org
to whatever your address is.  We might have to sue you over that. Otherwise the addrese 
should be relative.
