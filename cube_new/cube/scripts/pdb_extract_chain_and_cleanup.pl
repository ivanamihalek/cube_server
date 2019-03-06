#! /usr/bin/perl -w

use strict;
use warnings;
defined ( $ARGV[1]  ) ||
    die "Usage: $0   <pdb_file>  <seq_name>  [<chain_name> <output path>].\n";

my $pdb_file = $ARGV[0];
my $seqname = $ARGV[1];
my $query_chain_name ="" ;
my $path = "";

(defined $ARGV[2] && $ARGV[2] ne "-")  &&  ($query_chain_name =$ARGV[2]);
(defined $ARGV[3])  &&  ($path = $ARGV[3]);

if (!$path && $pdb_file=~ /\// ) {
    my @path_pieces = split "/", $pdb_file;
    pop @path_pieces;
    $path = join("/", @path_pieces);
}


open ( IF, "<$pdb_file") ||
    die "Cno $pdb_file: $!.\n";

#$exceptions = "ACE_PCA_DIP_NH2_LTA";

my %three2one = ( 'GLY', 'G', 'ALA', 'A', 'VAL', 'V', 'LEU','L', 'ILE','I',
		 'MET', 'M', 'PRO', 'P', 'TRP', 'W', 'PHE','F', 'SER','S',
		 'CYS', 'C', 'THR', 'T', 'ASN', 'N', 'GLN','Q', 'TYR','Y',
		 'LYS', 'K', 'ARG', 'R', 'HIS', 'H', 'ASP','D', 'GLU','E', 
		 'PTR', 'Y', 'SCY', 'C', 'TPO', 'T', 'MSE', 'M',  'HIE', 'H',
                 'CYM', 'C', 'HSD', 'H'); 

my %one2three = (   'G', 'GLY',  'A', 'ALA', 'V', 'VAL', 'L','LEU', 'I', 'ILE',
		 'M', 'MET',  'P', 'PRO', 'W', 'TRP', 'F','PHE', 'S', 'SER',
		 'C', 'CYS',  'T', 'THR', 'N', 'ASN', 'Q', 'GLN', 'Y','TYR',
		 'K', 'LYS', 'R',  'ARG', 'H', 'HIS', 'D', 'ASP', 'E','GLU'); 


my %seen = ();

my $res_ctr = 1;
my $old_res_seq = "";
my $old_res_name = "";
my $sequence     = "";
my $coordinates  = "";

while ( <IF> ) {

    last if ( /^ENDMDL/);
    #last if ( /^TER/);
    next if ( ! /^ATOM/ && ! /^HETATM/ );

    # chain: if given, must be present
    my $chain_name = substr ( $_,  21, 1) ;
    next if ( $chain_name =~ /\S/ && $query_chain_name &&   ($chain_name ne $query_chain_name) );

    # we don't care about alternative locations in this story
    my $alt_loc = substr $_,16, 1 ;  $alt_loc =~ s/\s//g;
    next if ( $alt_loc =~ /[BC]/ );

    # funny residues?
    my $res_name = substr $_,  17, 3; $res_name =~ s/\s//g;
    next if ( !defined $three2one{$res_name});

    #try to handle insertion code cases:
    my $res_seq   = substr $_, 22, 5;  $res_seq=~ s/\s//g;

    my $atom_name = substr $_, 12, 4; $atom_name=~ s/\s//g;
    next if (  defined $seen{"$res_seq $atom_name" } );
    $seen{"$res_seq $atom_name"} = 1;

    # if the chain field is empty, fill as $query_chain_name or  "A"
    my $new_line = $_;
    if ($chain_name eq " ") {
	    $query_chain_name || ($query_chain_name =  "A");
	    substr ($new_line,  21, 1) =  $query_chain_name;
    } else {
	    $query_chain_name = $chain_name;
    }

    substr ($new_line,  0, 6)  =  "ATOM  ";
    
    substr ($new_line,  17, 3) = $one2three{$three2one{$res_name}};
    # collect  coords
    # we want to get rid of \r (carriage return) that Windows and Mac introduce
    $new_line =~ s/\r/\n/g;
    $coordinates .= $new_line;
    
    $res_seq  = substr $_, 22, 5; $res_seq  =~ s/\s//g;

    next if ( ($res_seq eq $old_res_seq ) &&   ($res_name eq $old_res_name));


    # add the single-letter code to the sequence
    $sequence .= $three2one{$res_name};
    ($res_ctr %50 ) ||  ($sequence .= "\n");
    

    $old_res_seq  =  $res_seq;
    $old_res_name =  $res_name;
    $res_ctr++;
}


close IF;


#######################################################
if (! $sequence ) {
    print "chain $query_chain_name not found in $pdb_file or $pdb_file empty\n";
    exit(1);
}

#######################################################
# we won't go out of here without having a chain name
my $root_name  = $pdb_file;
if ($pdb_file=~ /\// ) {
    my @path_pieces = split "/", $pdb_file;
    $root_name = pop @path_pieces;
}
$root_name  =~ s/\.pdb$//g;

my $new_pdb  = $seqname.".pdb";
$path && ($new_pdb  = $path."/".$new_pdb);
my $seq_file = $seqname.".seq";
$path && ($seq_file = $path."/".$seq_file);

open (PDB, ">$new_pdb") || die "Cno $new_pdb: $!.\n";
print PDB $coordinates;
close PDB;

open (SEQ, ">$seq_file") || die "Cno $seqname: $!.\n";
print SEQ ">$seqname\n";
print SEQ $sequence."\n";
close SEQ;

exit(0);