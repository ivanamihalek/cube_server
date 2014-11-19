#!/usr/bin/perl -w
######################################################################
## Script : Specs.pl
## 
## 
## Author : Zhang Zong Hong, Ivana
## Date :   2010-2013
## Description : Get input from Specs server   
## Modifications : 
######################################################################

use strict;


# job types that the server is accepting
use constant CONSERVATION                      => 0;
use constant SPECIALIZATION_WITH_SEQS_PROVIDED => 1;
use constant SPECIALIZATION_SEQS_NOT_PROVIDED  => 2;


use specs_input;
use specs_html;
use specs_utils;
use specs_conservation;
use specs_specialization;

use DB_File;
use warnings;
use CGI;
#use CGI::Carp qw(carpout fatalsToBrowser);

use CGI qw(:standard -debug);
use CGI::Push qw(:standard);
use Data::Dumper;
use MIME::QuotedPrint;
use MIME::Base64;
use File::Copy;
use Spreadsheet::ParseExcel;
use Spreadsheet::ParseExcel::Format;
use IO::Handle;


# host machine  - used to set up the paths to third-party dependencies - see below
my $host = "bigmac";

# directory tree
my $dir              = "/Users/ivana/cube_server/";
my $scratchdir       = "/tmp";


# main application code
my $cube             = "$dir/bin/hyper_c";
my $specs            = "$dir/bin/specs";

# perlscripts
my $docx2txt          = "$dir/scripts/docx2txt.pl";
my $fasta_rename      = "$dir/scripts/fasta_rename_seqs.pl";
my $afa2msf           = "$dir/scripts/afa2msf.pl";
my $msf2afa           = "$dir/scripts/msf2afa.pl";
my $hc2xls            = "$dir/scripts/hc2xls.pl";
my $hc2pml            = "$dir/scripts/hc2pml.pl";
my $pdb_extract_n_clean = "$dir/scripts/pdb_extract_chain_and_cleanup.pl";
my $pdb2seq           = "$dir/scripts/pdb2seq.pl";
my $sort_by_taxonomy  = "$dir/scripts/sort_by_taxonomy.pl"; # needs $tax_attempt
my $tax_attempt       = "$dir/db/tax_attempt";
my $specs2pml         = "$dir/scripts/specs2pml.pl";
my $restrict          = "$dir/scripts/restrict_msf_to_query.pl";
my $specs2excel       = "$dir/scripts/specs2xls.pl";
my $reorder           = "$dir/scripts/reorder_fasta.pl";
# templates
my $cube_cmd_template = "$dir/cmd_template_cube";

# java
my $seqReport         = "$dir/bin/SeqReport.jar";
my $seqReportEE       = "$dir/bin/SeqReportEE.jar";


# third party 
my $muscle            = "$dir/bin/muscle";
my $dssp              = "$dir/bin/dssp";


my $mafft;
my $pymol;
my $zip;

if ($host eq  "reindeer") {
    $mafft             = "/usr/local/bin/mafft";
    $pymol             = "/cluster/apps/x86_64/bin/pymol";
    $zip               = "/usr/bin/zip";

} elsif ($host eq "bigmac") {
    $mafft             = "/usr/local/bin/mafft";
    $pymol             = "/Applications/molviz/MacPyMOL.app/Contents/MacOS/MacPyMOL";
    $zip               = "/usr/bin/zip";

} else {
    diehard ("SPECS","no setup for the host machine $host provided\n");
}


foreach ($scratchdir, $dir, $restrict, $specs){
    (-e $_) || diehard ("SPECS","$0: $_ not found\n");
}

my $cgi              = new CGI;
my $jobID;
my $new_job          = 1;
my $input_msf;
my $cmd;
my $cmd_specs;
my $my_id            = $$;
my $minimum_geneNum  = 2;


##################################################
## dteremine if this is is a new run or an update
#
if ( ! defined $cgi->param ("jobID") ) { # new run

    #here we add date to my_id to avoid the possible repeat of my_id
    my @date = split " ", `date`;
    my @time = split ":", $date[3];
    @date = split "-", `date +%F`;
    my $date_time = "$date[1]$date[2]";
    chomp($date_time);
    $date_time .= join "",@time;

    $jobID = "$date_time$my_id";

} else { # update

    $new_job = 0;
    $jobID   = $cgi->param ("jobID");
}


###################################################
my $jobdir = "$scratchdir/specs_$jobID";
$new_job   && `mkdir $jobdir`;


######################################################################################################
######################################################################################################
# process the incoming request
if ($new_job) {

    my ($errmsg, $ref_seq_name, $ref_group, $input_seq_files_ref,  $score_method, 
	$job_type,  $seq_not_aligned, $group_file, 
	$geneL_ref, $geneF, $seq_annotation_ref, $name_resolution_file, $alignment_file,
	$structure_file, $structure_name, $chainID, $structure_single_chain);
    
    ($errmsg, $ref_seq_name, $input_seq_files_ref, $score_method, 
     $job_type,  $seq_not_aligned,
     $geneL_ref, $geneF, $seq_annotation_ref, $structure_name, $chainID) = process_input_params($cgi,$jobdir,$docx2txt);

    ($errmsg eq '') || html_die ("Error processing the input parameters. $errmsg");

    ($errmsg, $ref_seq_name,  $ref_group, $alignment_file, $name_resolution_file, $group_file, 
     $structure_name, $structure_file, $structure_single_chain) = 
	 process_input_data ($jobdir, $job_type, $input_seq_files_ref, 
			     $seq_not_aligned, $ref_seq_name, $structure_name, 
			     $chainID, $pdb_extract_n_clean, $pdb2seq, 
			     $fasta_rename, $msf2afa, $mafft, $muscle, $reorder, 
			     $afa2msf, $restrict);

    ($errmsg eq '') || html_die ("Error processing the input. $errmsg");



    if ($job_type == CONSERVATION) {
	conservation ($jobID, $jobdir,  $ref_seq_name,   $alignment_file, $score_method,
		      $seq_not_aligned, $seq_annotation_ref, $name_resolution_file, 
		      $structure_file, $structure_name, $chainID, $structure_single_chain,  $dssp,
		      $specs, $specs2pml,  $specs2excel, $seqReport, $pymol, $zip);

    } else {
	specialization($jobID, $jobdir, $ref_seq_name,  $ref_group, $alignment_file, $group_file, $score_method,
		       $seq_not_aligned, $seq_annotation_ref, $name_resolution_file,
		       $structure_file, $structure_name,  $chainID, $structure_single_chain,  $dssp,
		       $cube, $cube_cmd_template, $hc2xls, $seqReportEE, $hc2pml, $pymol, $zip);
    }

# spit out previously calculated page
} else{

    print `cat $scratchdir/specs_$jobID/display.html`;
   
}


######################################################################################################
######################################################################################################
