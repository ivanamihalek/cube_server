#!/usr/bin/perl -w 

use strict;
use warnings;
use CGI;
use CGI::Push qw(:standard);
use CGI qw(:standard -debug);
use Data::Dumper;
use MIME::QuotedPrint;
use MIME::Base64;
use File::Copy;

#use lib '/home/zhangzh/struct_server/scripts';
use lib '/var/www/dept/bmad/htdocs/projects/EPSF/struct_server/scripts';
use MiscUtil;
use PostShow;

$| = 1; # perform flush after each write to STDOUT 

my $scratchdir    = "/tmp";

my $cgi  = new CGI;
my $htmlf;

if ( ! defined $cgi->param ("htmlf") ){
	diehard("display.cgi","htmlf not defined");
}
else {
    $htmlf = $cgi->param ("htmlf");
}
#my $htmlf = "$scratchdir/specs_$jobID/display.html";
#my $content;
open(FH, "<$htmlf") || die "Cno:$htmlf:$!";
while(<FH>){
    print $_;
}
close(FH);
