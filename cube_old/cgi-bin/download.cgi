#!/usr/bin/perl -wT  
 
use strict;
use warnings;
use CGI;
use CGI::Carp qw(carpout fatalsToBrowser);
use CGI::Push qw(:standard);
use CGI qw(:standard -debug);
#my $files_location;  
my $ID;  
my @fileholder;
my $downloadID; 
my $cgi = new CGI; 
 

 
$ID = $cgi->param("ID");
my @tmp = split(/\//, $ID);
$downloadID = $tmp[$#tmp];  


if ($downloadID eq '') {
print "Content-type: text/html\n\n";  
print "You must specify a file to download.";  
} else {  
 
#open(DLFILE, "<$ID") || Error('open', 'file');
open(DLFILE, "<$ID") || die "cno open, $ID"; 
@fileholder = <DLFILE>;  
close (DLFILE) || die "cno close, $ID"; 
#close (DLFILE) || Error ('close', 'file');  
 
 
 
print "Content-Type:application/x-download\n";  
print  "Content-Disposition:attachment;filename=$downloadID\n\n"; 
print @fileholder  
}
