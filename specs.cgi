#!/usr/bin/perl -w -I/var/www/dept/bmad/htdocs/projects/EPSF/struct_server/scripts/SendMail-2.09
######################################################################
## Script : Specs.pl
## 
## 
## Author : Zhang Zong Hong, Ivana
## Date :   2010-2013
## Description : Get input from Specs server   
## Modifications : 
######################################################################
#use FileHandle;
#use Switch;
#use POSIX qw(:sys_wait_h);
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
use Switch;
use warnings;
use CGI;
#use CGI::Carp qw(carpout fatalsToBrowser);

use CGI qw(:standard -debug);
use CGI::Push qw(:standard);
use Data::Dumper;
use SendMail;
use MIME::QuotedPrint;
use MIME::Base64;
use Mail::Sendmail;
use File::Copy;
use Spreadsheet::ParseExcel;
use Spreadsheet::ParseExcel::Format;
use IO::Handle;

use lib '/var/www/dept/bmad/htdocs/projects/EPSF/struct_server/scripts';
use MiscUtil;
use MolGfx;



# directory tree
my $dir              = "/var/www/dept/bmad/htdocs/projects/EPSF/specs_server";
my $scratchdir       = "/tmp";


# main application code
my $cube             = "$dir/bin/hyper_c";
my $specs            = "$dir/bin/specs";

# perlscripts
my $fasta_rename      = "$dir/scripts/fasta_rename_seqs.pl";
my $afa2msf           = "$dir/scripts/afa2msf.pl";
my $msf2afa           = "$dir/scripts/msf2afa.pl";
my $hc2xls            = "$dir/scripts/hc2xls.pl";
my $hc2pml            = "$dir/scripts/hc2pml.pl";
my $pdb_extract_chain = "$dir/scripts/pdb_extract_chain.pl";
my $pdb2seq           = "$dir/scripts/pdb2seq.pl";
my $sort_by_taxonomy  = "$dir/scripts/sort_by_taxonomy.pl"; # needs $tax_attempt
my $tax_attempt       = "$dir/db/tax_attempt";
my $specs2pml         = "$dir/scripts/specs2pml.pl";
my $restrict          = "$dir/scripts/restrict_msf_to_query.pl";
my $specs2excel       = "$dir/scripts/specs2xls.pl";

# templates
my $cube_cmd_template = "$dir/cmd_template_cube";

# java
my $seqReport         = "$dir/bin/SeqReport.jar";


# third party 
my $muscle            = "$dir/bin/muscle";
my $dssp              = "$dir/bin/dssp";

my $pymol             = "/cluster/apps/x86_64/bin/pymol";
my $zip               = "/usr/bin/zip";
my $jmol_folder       = "http://eopsf.org/cube/db/jmol";


foreach ($scratchdir,$dir,$restrict,$specs){
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

    my ($errmsg, $ref_seq_name, $input_seq_files_ref,  $score_method, 
	$job_type,  $seq_not_aligned, $group_file, 
	$geneL_ref, $geneF, $seq_annotation_ref, $name_resolution_file, $alignment_file,
	$structure_file, $structure_name, $chainID);
    
    ($errmsg, $ref_seq_name, $input_seq_files_ref, $score_method, 
     $job_type,  $seq_not_aligned,
     $geneL_ref, $geneF, $seq_annotation_ref, $structure_name, $chainID) = process_input_params($cgi,$jobdir);



    ($errmsg eq '') || html_die ("Error processing the input parameters. $errmsg");

    ($errmsg, $ref_seq_name, $alignment_file, $name_resolution_file, $group_file, 
     $structure_name, $structure_file) = process_input_data ($jobdir, $job_type, $input_seq_files_ref, 
							     $seq_not_aligned, $ref_seq_name,
							     $structure_name, $chainID, 
							     $pdb_extract_chain, $pdb2seq, 
							     $fasta_rename,  $msf2afa, $muscle, $afa2msf);

    ($errmsg eq '') || html_die ("Error processing the input. $errmsg");



    if ($job_type == CONSERVATION) {
	conservation ($jobID, $jobdir,  $ref_seq_name,   $alignment_file, $score_method,
		      $seq_not_aligned, $seq_annotation_ref, $name_resolution_file, 
		      $structure_file, $structure_name, $chainID,  $dssp,
		      $specs, $specs2pml, $restrict, $specs2excel, $seqReport, $pymol, $zip);

    } else {
	specialization($jobID, $jobdir, $alignment_file, $group_file, $score_method,
		       $seq_not_aligned, $seq_annotation_ref, $name_resolution_file,
		       $structure_file, $structure_name,  $chainID,  $dssp,
		       $cube, $cube_cmd_template, $hc2xls, $hc2pml, $pymol, $zip, $jmol_folder);
    }

# spit out previously calculated page
} else{

    print `cat $scratchdir/specs_$jobID/display.html`;
   
}


######################################################################################################
######################################################################################################
