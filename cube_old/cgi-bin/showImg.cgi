#!/usr/bin/perl -w

use strict;

use CGI;

my $errmsg;

my $cgi = new CGI;
($errmsg, my $filenm) = getCgiParams($cgi);
($errmsg eq '') or exit;


($errmsg, my $data) = slurp("$filenm");
($errmsg eq '') or exit;

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
