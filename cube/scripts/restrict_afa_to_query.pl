#! /usr/bin/perl -w
use strict;
use warnings FATAL => 'all';
use IO::Handle; #autoflush
# FH -> autoflush(1);

 
defined $ARGV[1]  ||
    die "Usage: restrict_afa_to_query.pl  <afa_file_name>  <protected sequence> [ ...<more protected seqs>... ]\n";

my $afa            = shift @ARGV;
my @protected_names = @ARGV;

my @names = ();
my %sequence = ();
my $name;
open ( AFA, "<$afa") ||
    die "Cno $afa: $!\n";

while ( <AFA> ) {
    chomp;
    if (/^>\s*(\S+)/ ) {
		$name = $1;
		push @names,$name;
		$sequence{$name} = "";
    } else  {
		s/[\.\#x]/\-/g;
		s/\s//g;
		$sequence{$name} .= $_;
    }
}
close AFA;


# sanity check:
@names || die "Error in $0: no seqs found.\n"; 

###########################################################
# turn the alignment into a table (first index= sequence, 2nd index= position
my $max_pos = -1;
my %array = ();
foreach   $name ( @names ) {
    @{$array{$name}} = split '', $sequence{$name};
    if ( $max_pos < length($sequence{$name}) ) {
		$max_pos = length($sequence{$name});
    }
}

$max_pos--;
my @delete;
foreach my $pos ( 0 .. $max_pos ) {
    
    $delete[$pos] = 1;
    for my $query_seq (@protected_names) {
		defined $array{$query_seq} || next;
		if ( $array{$query_seq}[$pos] !~ /[\-\.]/) {
			$delete[$pos] = 0;
			last;
		}
    }
}

my %seq_new = ();
foreach   $name ( @names) {
    $seq_new{$name} = "";
    foreach my  $pos ( 0 .. $max_pos ) {
		$delete[$pos]  ||  ($seq_new{$name} .= $array{$name}[$pos]);
    }
}


###########################################################
# output
foreach $name ( @names ) {
    print  ">$name\n";
    my $offset = 0;
	my $len = length($seq_new{$name} );
	while ($offset<$len) {
		print substr $seq_new{$name}, $offset, 70;
		print "\n";
		$offset += 70;
	}
}



0;
