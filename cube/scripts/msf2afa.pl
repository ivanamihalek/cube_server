#! /usr/bin/perl -w 
use strict;
use warnings;
use IO::Handle; #autoflush
use File::Copy; # copy a file (no kidding)

# FH -> autoflush(1);
defined $ARGV[0]  ||
    die "Usage: msf2afa.pl <msffile> \n";


my $home = `pwd`;
chomp $home;
my $name = $ARGV[0] ;

open ( MSF, "<$name" ) ||
    die "Cno: $name  $!\n";


while ( <MSF>) {
    last if ( /\/\// );
    last if ( /CLUSTAL FORMAT for T-COFFEE/ );
}
my @names = ();
my %seqs = ();

while ( <MSF>) {
    next if ( ! (/\w/) );
    chomp;
    my @aux = split;
    my $seq_name = $aux[0];
    if ( defined $seqs{$seq_name} ){
        $seqs{$seq_name} .= join ('', @aux[1 .. $#aux]);
    } else {
        $seqs{$seq_name}  = join ('', @aux[1 .. $#aux]);
        push @names, $seq_name;
    }
}

close MSF;

foreach my $seq_name ( @names ) {
    $seqs{$seq_name} =~ s/\./-/g;
    my @seq = split ('', $seqs{$seq_name});
    print  ">$seq_name\n";
    my $ctr = 0;
    for my $i ( 0 .. $#seq ) {
        print   $seq[$i];
        $ctr++;
        if ( ! ($ctr % 50) ) {
            print  "\n";
        }
    }
    print  "\n";
}

 
0;

