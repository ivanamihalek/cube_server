#! /usr/bin/perl -w
use strict;
use warnings;
use IO::Handle; #autoflush

defined ( $ARGV[0]  ) ||
    die "Usage: pdb_chain_rename.pl   <pdb_file>   [<chain_name>].\n";

my $pdbfile = $ARGV[0];
my  $query_chain_name ="" ;
defined $ARGV[1] && ($query_chain_name =$ARGV[1]) ;

open (IF, "<$pdbfile") || die "Cno $pdbfile: $!.\n";


    
while ( <IF> ) {

    last if ( /^ENDMDL/);
    next if ( ! /^ATOM/  );
    my $line = $_;
    my $chain_name = substr ( $line,  21, 1) ;
    if ( ! $query_chain_name ||   $chain_name eq " " ||
	$chain_name eq $query_chain_name ) {
	    print $line;
    }
}

close IF;
