#!/usr/bin/perl -w

use strict;

use File::Spec;
use CGI;

#use lib "/home/westleys/cgi-bin";
#use lib "/var/www/dept/bmad/htdocs/projects/EPSF/cgi-bin";
use lib "/var/www/dept/bmad/htdocs/projects/EPSF/struct_server/scripts";

use MiscUtil;
use MolGfx;
use PostShow;

my $errmsg;

my $cgi = new CGI;
($errmsg, my $filenm) = getCgiParams($cgi);
($errmsg eq '') or dieErrPage($cgi, "couldn't get CGI params: $errmsg");


($errmsg, my $data) = slurp("$filenm");
    ($errmsg eq '') or dieErrPage($cgi, "couldn't slurp zipfile: $errmsg");

    print("Content-Type:image/png\n");  
    print("\n");

    burp($data);
    exit;



sub getCgiParams {
    my ($q) = @_;
    my $cgiparam = $q->param("params");
    (defined $cgiparam) or return "CGI param not defined.";
    return ('', $cgiparam);
}

sub slurp {
    my ($file) = @_;
    local( $/ );
    open(my $fh, $file) or return "couldn't open: '$file'";
    return ('', scalar <$fh>);
}

sub burp {
    print($_[0]);
}
