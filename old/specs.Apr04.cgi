#!/usr/bin/perl -w -I/var/www/dept/bmad/htdocs/projects/EPSF/struct_server/scripts/SendMail-2.09
######################################################################
## Script : Specs.pl
## 
## 
## Author : Zhang Zong Hong, Ivana
## Date : December 2010
## Description : Get input from Specs server   
## Modifications : 
######################################################################
#use FileHandle;
#use Switch;
#use POSIX qw(:sys_wait_h);

use DB_File;
use strict;
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

#use lib '/home/zhangzh/cgi-bin';
use lib '/var/www/dept/bmad/htdocs/projects/EPSF/struct_server/scripts';
use MiscUtil;
use PostShow;
use MolGfx;

sub getParams(@);
sub getPngFile(@);
sub getHtmlHeader(@);
sub getHtmlBottom();
sub getHtmlBody(@);
sub getHtmlSpreadsheet(@);
sub getHtmlJmol(@);
sub Jmolscript(@);
sub getHtml(@);
sub runProfile(@);
sub generateCmdFile(@);
sub addAnnot(@);
sub deleteGap(@);
sub dieproc(@);


# directory tree
my $dir              = "/var/www/dept/bmad/htdocs/projects/EPSF/specs_server";
my $scratchdir       = "/tmp";


# main application code
my $cube             = "$dir/bin/hyper_c";
my $specs            = "$dir/bin/specs";

# perlscripts
my $afa2msf          = "$dir/scripts/afa2msf.pl";
my $get_orth         = "$dir/scripts/getOrth_one_cnm.pl";
my $hc2xls           = "$dir/scripts/hc2xls.pl";
my $hc2pml           = "$dir/scripts/hc2pml_com.pl";
my $pdb_extr_chain   = "$dir/scripts/pdb_extract_chain.pl";
my $pdb2seq          = "$dir/scripts/pdb2seq.pl";
my $sort_by_taxonomy = "$dir/scripts/sort_by_taxonomy.pl"; # needs $tax_attempt
my $tax_attempt      = "$dir/db/tax_attempt";
my $specs2pml        = "$dir/scripts/specs_cbcvg.pl";
my $restrict         = "$dir/scripts/restrict_msf_to_query.pl";
my $specs2excel      = "$dir/scripts/specs2xls.pl";

# templates
my $cmd_template     = "$dir/cmd_template";
my $cmd_tmp_cub      = "$dir/cmd_template_cube";

# java
my $seqReport        = "$dir/bin/SeqReport.jar";


# third party
my $muscle           = "$dir/bin/muscle";

my $pymol            = "/cluster/apps/x86_64/bin/pymol";
my $zip              = "/usr/bin/zip";
my $jmol_folder      = "http://epsf.bmad.bii.a-star.edu.sg/struct_server/jmol";


foreach ($scratchdir,$dir,$restrict,$cmd_template,$specs){
    (-e $_) || diehard ("SPECS","$0: $_ not found\n");
}

my $cgi  = new CGI;
my $jobID;
my $running;
my $input_msf;
my $cmd;
my $cmd_specs;
my $prms_string;
my $my_id = $$;
my $minimum_geneNum = 2;


##################################################
## dteremine if this is is a new run or an update
#
if ( ! defined $cgi->param ("jobID") ) { # new run

    $running = 0;

    #here we add date to my_id to avoid the possible repeat of my_id
    my @date = split " ", `date`;
    my @time = split ":", $date[3];
    @date = split "-", `date +%F`;
    my $date_time = "$date[1]$date[2]";
    chomp($date_time);
    $date_time .= join "",@time;

    $jobID   =  "$date_time$my_id";

} else { # new ruupdate

    $running = 1;
    $jobID = $cgi->param ("jobID");
  
}

###################################################
my $jobdir = "$scratchdir/specs_$jobID";
$running || `mkdir $jobdir`;

my $cmd_file = "$jobdir/cmd"; #cmd file for hyper cube

my $htmlf="$jobdir/display.html";
my $url;
my $gene_notfound=0;
if(!$running){

    my ($errmsg, $query_nm, $input_fpath, $input_fn, $score_method,
	$hyper,$group_f,$seq_aligned,$similarity,
	$geneL_ref, $geneF, $annotation_file,$seq_annot_ref,$structure,$struct_name) = getParams($cgi,$jobdir);

    ($errmsg eq '') || dieErrPage($cgi, "couldn't get CGI params: $errmsg");
    

    my $muscle_out_msf = "$jobdir/$input_fn\.msf";
    my $restrict_msf = "$jobdir/$input_fn\.restr";
    my $score_eachmethod = "$jobdir/$input_fn\.$score_method";
    my $png_f = "$jobdir/$input_fn";
    my $excel_out = "$jobdir/$input_fn";
    my $para_string;
    my $score_f = "$jobdir/specs_out\.score";

    if(defined($query_nm)&&$query_nm){
	if($seq_aligned){
	    if(`grep " Name:" $input_fpath`){
		if(!`grep "Name: $query_nm" $input_fpath`){
		    diesoft("query is not included in the alignment file,Please give a correct query name!");
		}
	    }
	    else{
		diesoft("The input sequnce file is not in MSF format!");
	    }
	}
	else{
	    if(`grep ">" $input_fpath`){
		if(!`grep ">$query_nm" $input_fpath`){
		    diesoft("query is not included in the alignment file,Please give a correct query name!");
		}
	    }
	    else{
		diesoft("The input sequnce file is not in FASTA format!");
	    }
	}
    }

    if(!$seq_aligned && $hyper != 2){#alignment1
    
	$cmd = "$muscle -in $input_fpath -msf -out $muscle_out_msf";

	system($cmd) && diehard("specs", "error running $cmd");
    }


    if($hyper==0){
    
        ###################################################
        # SPECS
        ###################################################
	my $pdbf;
	my $specs_out     = "outn $jobdir/specs_out";
	my $qry           = "query " . " $query_nm";
	my $align_msf     = "align $restrict_msf";
	my $method_string = "method " . $score_method;


	if ($structure)    {   
	    $pdbf = "pdbf $structure";
	}

	#############################################
	# restrict the sequence to the query -- so why is there a mismatch btw the spread sheet and jpg with Tin2?
	# 
	if( !$seq_aligned) {#if the input file is not aligned, we use the output of above alignment1
	    $cmd = "$restrict  $muscle_out_msf $query_nm > $restrict_msf";

	} else { #if the input is aligned,we restrict the input directly
	    $cmd = "$restrict  $input_fpath $query_nm > $restrict_msf";
	}
	    
	`$cmd`;


	#############################################
	# create the cmd file
	# 
	open(FH, "<$cmd_template") || diehard("specs", "cno:$cmd_template,$!");
	undef $/;
	$prms_string = <FH>;
	$/="\n";
	close(FH);

	$prms_string =~ s/align/$align_msf/;
	$prms_string =~ s/query/$qry/;
	$prms_string =~ s/outn/$specs_out/;
	$prms_string =~ s/method/$method_string/;
	if($structure){
	
	    $prms_string =~ s/!pdbf/$pdbf/;
	}
    
	$cmd_specs = "$jobdir/specs_cmd";

	open(FH, ">$cmd_specs") || diehard("specs","Cno:$cmd_specs, $!\n");
	undef $/;
	print FH $prms_string;
	$/="\n";
	
	close(FH);


	#############################################
	# run specs
	# 
	my $stdout = "$jobdir/specs.stdout";
	my $stderr = "$jobdir/specs.stderr";

	$cmd = "$specs $cmd_specs 1>$stdout 2>$stderr";
    
	system($cmd);


    
	if( $errmsg = `grep \"Structure/alignment mismatch\" $stderr`){
	    chomp($errmsg);
	    diesoft("$jobdir:$errmsg the query sequence must be the same as sequence of uploaded structure");

	}
	if($errmsg = `grep \"Unrecognized amino acid code\" $stdout`){
	    chomp($errmsg);
	    diesoft("$errmsg in the uploaded strucure");
	}
    
   
    

	###############################################################################################
	#generate picture
    
	`awk \'\$1 \!= \"\%\" \{print \$5 \"  \" \$3 \"   \" \$1\}\' $score_f > $score_eachmethod`; 
	

	$cmd = "java -jar $seqReport $score_eachmethod $jobdir/$input_fn";

	my @resi_cnt = split(/\s/,`wc -l $score_eachmethod`);
	my $num_resi = $resi_cnt[0];
	my $range = 400;
	($errmsg, my $png_ref) = getPngFile($num_resi,$png_f,$score_eachmethod, $range);

	($errmsg eq "") || diehard("specs", $errmsg);
    
    
	############################################################################
	#generate excel spreadsheet
	$cmd = "$specs2excel $jobdir/specs_out.score $jobdir/$input_fn";

	system($cmd) && diehard("specs", "Error running $cmd:$!");

	$excel_out .= ".xls";

	###########################################################################
	#generate pymol session
	#my $script_rvet = "$jobdir/$query_nm.rvet.pml";
	#my $script_entr = "$jobdir/$query_nm.entr.pml";
	my $script = "$jobdir/$query_nm.pml";
	my ($zipfile,$session);
    
	if($structure){
	    $cmd = "$specs2pml $score_method $score_f $structure $script"; 
	    #$cmd = "$specs2pml $score_method specs_out.score $structure $script";
	    #printResult($cmd);
	    system($cmd) && diehard("SPECS", "Error running $cmd:$!");

	
	    $cmd = "$pymol -qc -u $script > /dev/null";
	    #printResult($cmd);
	    system($cmd) && diehard("SPECS", "Error running $cmd $!");


	    $session = $script;
	    (($session =~ s/\.pml$/\.pse/)==1)||diehard("specs", "Can not construct session name:$cmd");
	    $zipfile = "$session.zip";
	    $cmd = "$zip -j $zipfile $session > /dev/null";
	
	    system($cmd) && diehard("SPECS", "Error running $cmd");


	}
	###########################################################################
	#zip the how directory
	my $dirzipfile = "$jobdir.zip";
	$cmd = "$zip -r $dirzipfile $jobdir > /dev/null";
	system($cmd) && diehard("SPECS", "Error running $cmd");

	############################################################################
	#display output
	#($errmsg, my $html)=getHtml($excel_out,$png_ref, $num_resi, $range);
	#($errmsg eq "") || diehard("specs", $errmsg);

	($errmsg, my $html_header) = getHtmlHeader();
	($errmsg eq "") || diehard("specs", $errmsg);
    
	($errmsg, my $html) = getHtmlBody($score_f, $excel_out, $zipfile, $dirzipfile,$png_ref);
	($errmsg eq "") || diehard("specs", $errmsg);

	($errmsg, my $html_bottom)=getHtmlBottom();
	($errmsg eq "") || diehard("specs", $errmsg);

	print "$html_header$html$html_bottom";
	open(FH,">$htmlf") || diehard("specs","Cno:$html");
	print FH "$html_header$html$html_bottom";
	close(FH);

    } else{
        ########################################################################
        #CUBE
        #######################################################################
	my($almt, $group,$outnm,$xls_fnm, $almt_f);
	my $pdbf = 0;
	my $struct_nm = 0;
	my @fnm_seq = ();
	my @fnm_seq_alt =  ();
	my $kidpid;
	my $stdout = "$jobdir/cube.stdout";
	my $stderr = "$jobdir/cube.stderr";

	my $number_of_final_gene;
	my $number_of_annot_gene;
	
	if($structure){
	    $pdbf = "pdbname $structure";
	    $struct_nm = "struct_n $struct_name";
	   
	}

	if(!defined($kidpid=fork())){
	    diehard ("cube","cannot fork: $!");
	}
	elsif($kidpid == 0) {
       
	    if($hyper==1){

		############################################################################
		#by seuquence
		###########################################################################
		my $group_nm_cnt = `grep "name" $group_f | wc -l`;
		if($group_nm_cnt > 1){
		    if($seq_aligned){
			#$almt_f = "$jobdir/$input_fpath";
                        $almt_f = $input_fpath;
			$almt = "almtname $input_fpath";
		    }
		    else{
			$almt_f = $muscle_out_msf;
			$almt = "almtname $muscle_out_msf";
		    }
		    $group = "groups $group_f";
		    $outnm = "outname $jobdir/out";
		}
		elsif($group_nm_cnt==0){
		    dieproc("The formatting of your group file is wrong! See example file","",0);
		}
		elsif($group_nm_cnt==1){
		    dieproc("The number of group is not enough, at least two groups should be included!", "", 0);
		}
	    }
	    else{
		#############################################################
		#by gene name
		###########################################################

		my $geneL_fnm = "$jobdir/gene.list";
		my $profile = "$jobdir/alignment.afa";
	    
	    
		if(defined(@$geneL_ref) && @$geneL_ref){
		    if(($#$geneL_ref+1)<$minimum_geneNum){
			dieproc("The number of gene (1) is too small to perform comparative analysis.","", 0);
		    }
	
		    open(FH, ">$geneL_fnm")||dieproc("cno: $geneL_fnm:$!","",0);
		    foreach my $nm(@$geneL_ref){
			print FH "$nm\n";
		    }
		    close(FH);
		}
		else{
		    my $num = `wc -l $geneL_fnm`;
		    if($num <$minimum_geneNum){
			dieproc("The number of gene (1) is too small to perform comparative analysis","",0);
		    }
		    open(FH, "<$geneL_fnm")||dieproc("cno: $geneL_fnm:$!","",0);
		    while(<FH>){
			chomp($_);
			push(@$geneL_ref,$_);
		    }  
		    close(FH);
		}
	   # my $start = time();
		my $cmd = "$get_orth $geneL_fnm $jobID > $jobdir/notfound.txt";
	    
	    
		(system($cmd)) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
	    
		#check if the left over gene is less then 2
		my $num_notfound = `wc -l $jobdir/notfound.txt | awk \'\{print \$1\}\'`;
		chomp($num_notfound);
	
		$gene_notfound="";
		my @genelist_final;
		#my $t = time()-$start;
	    
	    
		if($num_notfound){
		    $gene_notfound = `cat $jobdir/notfound.txt`;
		    chomp($gene_notfound);
		    if(($#$geneL_ref-$num_notfound+1) < $minimum_geneNum){
			my $errmsg = "The following genes are not found:<br>$gene_notfound<br>" .
			    "\(Note: Cube currently accepts only human genes".
			    "If you are sure the gene exists in humans, please try an alternative name." .
			    "Contact us if the problem persists.\)<br>" . 
			    "The remaining number of genes (1) is too small to perform comparative analysis";
			dieproc($errmsg,"",0);
		    }


		}

	
		if($gene_notfound ne ""){
	            my @g_notfound = split("\n", $gene_notfound);
		    my @tmp_holder = @$geneL_ref;
			
		    foreach my $g(@g_notfound){	
			@genelist_final = grep(!/\b$g\b/, @tmp_holder);#grep(!/\b$gene_notfound\b/, @$geneL_ref);
		        @tmp_holder = @genelist_final;
	            }
		       
		    foreach my $g(@genelist_final){
			my $tmpf = "$jobdir/tmp.fasta";
			$cmd = "$sort_by_taxonomy $jobdir/$g.fasta > $tmpf"; #sorting
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd", 1);
			$cmd = "mv $tmpf $jobdir/$g.fasta";
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);

			$cmd = "$muscle -in $jobdir/$g.fasta -out $jobdir/$g.afa";
		    
			push(@fnm_seq,"$jobdir/$g.fasta");
			push(@fnm_seq_alt,"$jobdir/$g.afa");
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
		    
			$cmd = "$sort_by_taxonomy $jobdir/$g.afa > $tmpf"; #sorting
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
			$cmd = "mv $tmpf $jobdir/$g.afa";
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
		    
		    }
		    $number_of_final_gene = $#genelist_final+1;
		    my ($err) = runProfile(\@genelist_final,$profile);

		    ($err eq "")||dieproc($err,"",0);
		
	
		}
		else{
		
		    foreach my $g(@$geneL_ref){

			my $tmpf = "$jobdir/tmp.fasta";
			$cmd = "$sort_by_taxonomy $jobdir/$g.fasta > $tmpf"; #sorting
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
			$cmd = "mv $tmpf $jobdir/$g.fasta";
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);

			$cmd = "$muscle -in $jobdir/$g.fasta  -out  $jobdir/$g.afa";
		    
			push(@fnm_seq,"$jobdir/$g.fasta");
			push(@fnm_seq_alt,"$jobdir/$g.afa");
			(system($cmd)) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);

			$cmd = "$sort_by_taxonomy $jobdir/$g.afa > $tmpf"; #sorting
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
			$cmd = "mv $tmpf $jobdir/$g.afa";
			system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
		    
		    }
		    $number_of_final_gene = $#$geneL_ref+1;
		    my ($err) = runProfile($geneL_ref,$profile);
		    ($err eq "")||dieproc($err,"",0);
		
		}
	    
		#system($cmd) && diehard("SPECS", "Error running $cmd");
	
	    
   
		$group_f = "$jobdir/group";
		$almt_f = "$jobdir/alignment_profile.msf";
	
		#########################################################
		#generate a group file
		########################################################
	
	
		foreach my $fasta_fnm(@fnm_seq){
		    my $nmf = $fasta_fnm;
		    $nmf =~ s/(\.fasta)$//g;
		    my @tmp = split(/\//,$nmf);
		    my $gene = $tmp[$#tmp];
		    $cmd = "echo \"name $gene\" >> $group_f";
		    system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
		    $cmd = "cat \"$nmf\.name\" >> $group_f";
		    system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
		}
	
	
		#########################################################
		if($structure){
		    my $struct_seq_f = "$jobdir/$struct_name.fasta";
		    $cmd = "$pdb2seq $structure > $struct_seq_f";
		    system($cmd);
		    my $tmpfile = "$jobdir/tmp.afa";
		    `cp $profile $tmpfile`;
		    `$muscle -profile -in1 $tmpfile -in2 $struct_seq_f -out $profile`;
		    `mv $tmpfile`;
		
		}
		$cmd = "$afa2msf $profile > $jobdir/alignment_profile.msf";
	
	
		system($cmd) && dieproc("Fatal error encountered, admin has been notified","Error running $cmd",1);
		########################################################
	
	
		$group = "groups $group_f";
		$almt = "almtname $almt_f";
		$outnm = "outname $jobdir/out";
	    }
   
  
	    ($errmsg) = generateCmdFile($cmd_tmp_cub, $cmd_file, $almt, $group, $outnm,$pdbf,$struct_nm,$similarity);
	    ($errmsg eq "") || dieproc($errmsg,$errmsg,1);
    
	    $cmd = "$cube $cmd_file 1> $stdout 2> $stderr";
	    `$cmd`;
	    if(`grep '^Structure' $stderr`){
		my $err = "<b>Error:</b> structure $struct_name not found in the alignment file";
		my $header = getHtmlHeader();
		my $body = getHtmlBody($err);
		my $bottom = getHtmlBottom();
		open(FH, ">$htmlf")||dieproc("cno:$htmlf","Cno:$htmlf",1);
    
		print FH "$header$body$bottom";
		close(FH);
		exit;
	    }
	    $number_of_annot_gene = keys %$seq_annot_ref;
	

	    my($ermsg,$rank_annot_file)=addAnnot("$jobdir/out.score",$seq_annot_ref,$almt_f);
	    my $file_lessgap;
	    if($ermsg){
		dieproc($ermsg,$ermsg,1);
	    }
	    else{
	        
		my $err;
		if(-s $rank_annot_file){
		    ($err, $file_lessgap) = deleteGap($rank_annot_file);

		    #$cmd = "$hc2xls $rank_annot_file $jobdir/out";
		    
		}
		else{
		    ($err, $file_lessgap) = deleteGap("$jobdir/out.score");
		    #$cmd = "$hc2xls $jobdir/out.score $jobdir/out";
		    
		}
		($err)&&dieproc($err, $err, 1);
		$cmd = "$hc2xls $file_lessgap $jobdir/out";
	    }
	    `$cmd`;
	
	
    
	    my $xls = "$jobdir/out.xls";
	    my $score = "$jobdir/out.score";
	    my $pymolscript = "$jobdir/out.pml";
	    my $chimerascript_specs = "$jobdir/out_specs.com";
	    my $chimerascript_cons = "$jobdir/out_cons.com";
	    
	    if($structure){
	    
		my $cmd = "$hc2pml rvet $score $structure $pymolscript";
		#my $cmd = "$hc2pml rvet $file_lessgap $structure $pymolscript";
	    
		system($cmd) && dieproc("Fatal error encountered, admin has been notified:","Error running $cmd",1);
		my($err) = molgfxRunScript("pymol", $pymolscript);
		($err eq "") || dieproc($err,$err,1);
		($err) = molgfxRunScript("chimera", $chimerascript_specs);
		($err eq "") || dieproc($err,$err,1);
		($err) = molgfxRunScript("chimera", $chimerascript_cons);
		($err eq "") || dieproc($err,$err,1);
	    }
    
	    #####################################################
	    #generate header
	    ##################################################
	    my $html_header;
	    if($structure){
		($errmsg, $html_header) = getHtmlHeader(1);
	    }
	    else{
		($errmsg, $html_header) = getHtmlHeader(0);
	    }
	    ($errmsg eq "") || dieproc($errmsg,"",0);
    
	    ###################################################
	    #generate body
	    ###################################################
	    my $html_body= "";
	
	    #zip the whole directory
	    my $dirzipfile = "$jobdir.zip";
	    $cmd = "$zip -j $dirzipfile $jobdir/* > /dev/null";
	    system($cmd) && dieproc("Fatal error encountered, admin has been notified.","Error running $cmd",1);

	    #zip the alignment file
	    
	    my $alignment_file_zip = "$jobdir/alignment.afa.zip";
	    if($hyper != 1 && $hyper != 0){
		$cmd = "$zip -j $alignment_file_zip";
	    
		foreach my $file(@fnm_seq_alt){
		    $cmd .= " $file";
		}
		$cmd .= " > /dev/null";
	    
		system($cmd) && dieproc("Fatal error encountered, admin has been notified.","Error running ~~$cmd",1);
	    }
	    #if($hyper != 1){
		#foreach my $f(@fnm_seq){
	    
		    #($errmsg, my $html) = getHtmlBody($f);
		    #($errmsg eq "") || dieproc($errmsg,$errmsg,1);
		    #$html_body .= $html;
		#}
	    #}
	    if(-s "$jobdir/notfound.txt"){
		#my @test = splilt(/\n/,$gene_notfound);
		$gene_notfound = `cat $jobdir/notfound.txt`;
		chomp($gene_notfound);
		$gene_notfound =~ s/\n/,/;
		$gene_notfound .= " is/are not found in our database";
	    }
	    my $html_xls_score;
	    my $html_spreadsheet;

	    my ($html_pyml,$html_chi_specs, $html_chi_cons);
	    my $html_jmol = "";
	    my $pymsession = $pymolscript;
	    $pymsession =~ s/pml/pse/;

	    my $chisession_specs = $chimerascript_specs;
	    $chisession_specs =~ s/.com/.py/;

	    my $chisession_cons = $chimerascript_cons;
	    $chisession_cons =~ s/.com/.py/;
	    if($gene_notfound){
		if($structure){
		    ($errmsg, $html_xls_score) = getHtmlBody($xls,$alignment_file_zip,$score,$dirzipfile,$gene_notfound,
							     "$pymsession.zip","$chisession_specs.zip","$chisession_cons.zip");
		}
		else{
		    ($errmsg, $html_xls_score) = getHtmlBody($xls,$alignment_file_zip,$score,$dirzipfile,$gene_notfound);
		}
	    }
	    else{
		if($structure){
		    ($errmsg, $html_xls_score) = getHtmlBody($xls,$alignment_file_zip,$score,$dirzipfile,
							     "$pymsession.zip","$chisession_specs.zip","$chisession_cons.zip");
		}
		else{
		    ($errmsg, $html_xls_score) = getHtmlBody($xls,$alignment_file_zip,$score,$dirzipfile);
		}
	    }
	    ($errmsg eq "") || dieproc($errmsg,$errmsg,1);


	    #####################################################
	    #display downloading pymol session
	    ###################################################
	    #my ($html_pyml,$html_chi_specs, $html_chi_cons);
	    #my $html_jmol = "";
	    
	    if($structure){
		#my $pymsession = $pymolscript;
		#$pymsession =~ s/pml/pse/;

		#my $chisession_specs = $chimerascript_specs;
		#$chisession_specs =~ s/.com/.py/;

		#my $chisession_cons = $chimerascript_cons;
		#$chisession_cons =~ s/.com/.py/;

		#($errmsg, $html_pyml) = getHtmlBody("$pymsession.zip","$chisession_specs.zip","$chisession_cons.zip");
		#($errmsg eq "") || dieproc($errmsg,$errmsg,1);

		#($errmsg, $html_chi_specs) = getHtmlBody("$chisession_specs.zip");
		#($errmsg eq "") || dieproc($errmsg,$errmsg,1);

		#($errmsg, $html_chi_cons) = getHtmlBody("$chisession_cons.zip");
		#($errmsg eq "") || dieproc($errmsg,$errmsg,1);

		($errmsg, $html_jmol) = getHtmlJmol($jmol_folder,$pymolscript);
  
	    }
	    #$html_body .= $html_pyml;
	    #$html_body .= $html_chi_specs;
	    #$html_body .= $html_chi_cons;

	    #########################################################
	    #display excel spread sheet as a webpage
	    #########################################################
	    ($errmsg, $html_spreadsheet) = getHtmlSpreadsheet($xls, $number_of_final_gene, $number_of_annot_gene);
	    ($errmsg eq "")||dieproc($errmsg,$errmsg,1);
	    $html_body .= "$html_xls_score$html_spreadsheet";

	    $html_jmol .= $html_body;
	    $html_body = $html_jmol;

    
	    ####################################################
	    #generate bottom
	    ###################################################

	    ($errmsg, my $html_bottom)=getHtmlBottom();
	    ($errmsg eq "") || dieproc($errmsg,$errmsg,1);
    
	    #################################################
	    #$htmlf = "$jobdir/display.html";
	    open(FH, ">$htmlf")||dieproc("cno:$htmlf","cno:$htmlf",1);
	    
	    print FH "$html_header$html_body$html_bottom";
	    close(FH);
	}
    
	my $refresh_period = 2;
    
	$url = "http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/cube/display.cgi?htmlf=$htmlf";
	my $meta_string = "http-equiv=\"refresh\" content= \"$refresh_period;url=$url\"";
    
   
	if(!(-e $htmlf)){
	    #while($kidpid){
	
	
	
	    print "Content-type: text/html\n\n";
	    print "<html><head><meta $meta_string/>\n";
	    print "<style type=\"text/css\">\n";

	    print "\.style \{\n";
	    print "font-family: \"Courier New\"\;\n";
	    print "font-size: medium\;\n";

	    print "\}\n</style>\n";
	    print "</head> \n<body>";

	    #print "<body>processing....$jobID</body></html>";
            print "<table width=\"750\"  border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\">\n";
	    print "<tr>\n";
	    print "<td width=\"750\"><img src=\"http://epsf.bmad.bii.a-star.edu.sg/Image/s_body_top2.jpg\">\n";
	    print "</td>\n";
	    print "</tr>\n";		
    	    print "<tr>\n";
      	    print "<td width=\"750\">";
            print "<table width = \"100%\" border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" background=\"http://epsf.bmad.bii.a-star.edu.sg/Image/s_body_bg2.jpg\">\n";
            print " <tr><td>\&nbsp\;</td><td>\&nbsp\;</td>\n";
            print "<td>";
            print "processing....$jobID</td>\n";
            print "</tr>\n";
            print "</table>\n";
	    print "</td>\n";
	    print "</tr>\n";
            print "<tr>\n";
            print "<td width=\"750\">\n";
            print "<img src=\"http://epsf.bmad.bii.a-star.edu.sg/Image/s_body_bottom2.jpg\">\n";	
	    print "</td>\n";
	    print "</tr>\n";
            print "</table>\n";
            print "</body></html>";



	    
	    close STDIN; 
	    close STDOUT;
	    close STDERR;
    
	
	}
    

    }
}
else{
    my $displayfile = "$scratchdir/specs_$jobID/display.html";
    print "Content-type: text/html\n\n";
    print "<html>\n";
    print "<head>\n";
   
    print "<title>specs</title>\n";
    print "</head>\n";
    print "<frameset rows=\"120,\*\" frameborder=\"NO\" border=\"0\" framespacing=\"0\">\n";
    print "<frame src=\"../../cube/menu.html\" name=\"topFrame\" scrolling=\"NO\" noresize >\n";
    print "<frame src=\"./display.cgi?htmlf=$displayfile\" name=\"mainFrame\">\n";
    print "</frameset><noframes>\n<body>\n</body></noframes>\n</html>\n";
   
}


sub getParams(@){
    #print "Content-type: text/html\n\n";
    #foreach (sort keys %ENV)
    #{
	#print "<b>$_</b>: $ENV{$_}<br>\n";
    #}


    my ($q,$jobdir) = @_;
    my $cube;
    my (@annotation_geneN,@annotation_range, @annotation_infor);
    my %seq_annotation=();
    my $similarity_ckbox = 0;
    #default method for specs is rvet
    my $method = "rvet";

    #my $annotation_fileN="$jobdir/ann.txt";
    my $annotation_fileN = 0;
    #print"$annotation_fileN\n";

    if(defined($q->param("group"))){
	#cube with sequence as input
	$cube = 1;
    }
    elsif($q->param("geneList")||$q->param("geneNF")){
	#cube with gene name as input
	#my $test = $q->param("geneNF");
	#printResult("222 $test");
	$cube = 2;
    }
    else{
	#specs
	$cube = 0;
    }


    my ($upload_fhd,$fasta_fn,$in_fasta,$in_group,$struct_nm);
    my @geneList = ();
    #my $mthd = 0;
    my $qry_nm = 0;
    my $group_f = 0;
    my $gene_nm_file = 0;
    my $aligned = 0;
    my $structure_f = 0;
    
    if(defined($q->param("similarity")) && $q->param("similarity")){
	$similarity_ckbox = $q->param("similarity");
	
    }
    if($cube != 2){
	$fasta_fn = $q->param("fnm"); 

    
	my @tmp = split(/\\/, $fasta_fn);
	$fasta_fn = $tmp[$#tmp];
	$in_fasta = "$jobdir/$fasta_fn";
	
	if($cube != 1){ #specs requires query name
	    $qry_nm = $q->param("qry_nm");
	    
	}

	#$group_f = 0;
	
	if(defined($q->param("group"))){
	    $group_f = $q->param("group");
	    
	    if(!$group_f){
		return("Please upload a group file");
	    }
	    @tmp = split(/\\/, $group_f);
	    $in_group = "$jobdir/$tmp[$#tmp]";
	}
	
	
	
	if(defined($q->param("ckb")) && $q->param("ckb")){
	    $aligned = $q->param("ckb");
	    
	}
	#$qry_nm =~ s/\s//g;
	#$qry_nm = uc($qry_nm);

	$upload_fhd = $q->upload("fnm");
	(defined $upload_fhd) || return "File handle not define";
	open(OF, ">$in_fasta") || return "Cno: $in_fasta:$!\n";
	undef $/;
	print OF <$upload_fhd>;
	$/ = "\n";
	close(OF);
	
	if($qry_nm){
	    (`grep $qry_nm $in_fasta`) || return "Query name is not in the sequence file";
	}

	if(defined($q->param("group"))&&$q->param("group")){
	    $upload_fhd = $q->upload("group");
	    open(OF, ">$in_group") || return "Cno $in_group:$!\n";
	    undef $/;
	    print OF <$upload_fhd>;
	    $/ = "\n";
	    close(OF);
	}
    }
    else{
	#printResult("cube=$cube");
	$gene_nm_file = "$jobdir/gene.list";
	if(defined($q->param("geneList")) && $q->param("geneList")){
	    my $tmp_genel = $q->param("geneList");
	    $tmp_genel =~ s/\s//g; 
	    @geneList = split(/,/, $tmp_genel);
	}
	elsif(defined($q->param("geneNF")) && $q->param("geneNF")){
	    my $fn=$q->param("geneNF");
	   
	    $upload_fhd = $q->upload("geneNF");
	
	
	    (defined $upload_fhd) || return ("File handle not defined");
	   
	    open(OF, ">$gene_nm_file") || return "Cno:$gene_nm_file:$!";
	    undef $/;
	    print OF <$upload_fhd>;
	    $/ = "\n";
	    close(OF);
	}

	
	if(defined($q->param("annotation"))&&$q->param("annotation")){
	    my (@gnm_ary, @range_ary, @inf_ary);
	    
	    $annotation_fileN="$jobdir/ann.txt";
	    my @input_names = $q->param();
	    foreach my $nm(@input_names){
		if($nm =~ /^gene_name/){
		    my $tp = $q->param($nm);
		    if(defined($tp)){
			
			push(@annotation_geneN, $tp);
			
		    }
		}
		elsif($nm =~ /^range/){
		    my $tp = $q->param($nm);
		    if(defined($tp)){
			
			push(@annotation_range, $tp);
			
		    }
		}
		elsif($nm =~ /^information/){
		    my $tp = $q->param($nm);
		    if(defined($tp)){
			
			push(@annotation_infor, $tp);
		    }
		}
	    }
	    

	    open(OFH, ">$annotation_fileN") || return "Cno:$annotation_fileN:$!";
	    for my $i(0..$#annotation_geneN){
		
		
		my @range_ary = ();
		my @annotation_ary = ();
		#if(@geneList){ 
                    #we check if the annotation gene exists in gene list
			#if(!grep(/\b$annotation_geneN[$i]\b/,@geneList)){
			    #return("$annotation_geneN[$i] not in your gene list");			    
			#}
		    #}
		#elsif(!`grep $annotation_geneN[$i] $gene_nm_file`){ 
                    #if user upload a gene list file check annotation gene name exist in the fiel
		    #return("$annotation_geneN[$i] not in your gene file");
		#}
		
		if($annotation_geneN[$i] ne "" && $annotation_range[$i] ne "" && $annotation_infor[$i] ne ""){
		    if(($annotation_range[$i] !~ /-/) && ($annotation_range[$i] !~ /,/)){
		    
			push(@range_ary,$annotation_range[$i]);
			push(@annotation_ary,$annotation_infor[$i]);
		    }
		    elsif(($annotation_range[$i] =~ /-/) || ($annotation_range[$i] =~ /,/)){	
		    
			
			my @tmp_holder = split(/,/, $annotation_range[$i]);
		    
			foreach my $elt(@tmp_holder){
			    if($elt !~ /-/){
				push(@range_ary,$elt);
				push(@annotation_ary,$annotation_infor[$i]);
			    }
			    else{
				my @tmp=split(/-/,$elt);
				my $start=$tmp[0];
				my $end = $tmp[1];
				my $range_length = $end-$start+1;
				for (my $cnt = 0; $cnt < $range_length; $cnt++){
				    my $pos = $start+$cnt;
				    push(@range_ary,$pos);
				    push(@annotation_ary,$annotation_infor[$i]);
			   
				}
			    }
			}
		    }
	
	
		    if(!defined($seq_annotation{$annotation_geneN[$i]}{'range'})){
			$seq_annotation{$annotation_geneN[$i]}{'range'}=[@range_ary];
		    
			$seq_annotation{$annotation_geneN[$i]}{'annotation'}=[@annotation_ary];
		    
		    }
		    else{
			#here to test if the certain range already has had an annotation, 
		       
			my $index = "";
			for(my $cnt=0; $cnt<=$#range_ary; $cnt++){
			    $index = "";
			    ($index) = grep ${$seq_annotation{$annotation_geneN[$i]}{'range'}}[$_] 
				eq $range_ary[$cnt], 0..$#{$seq_annotation{$annotation_geneN[$i]}{'range'}};
			    if($index ne ""){#certain range has had been defined, appending the new annotation with comma as a separator
				#printResult("$index ..$annotation_ary[$cnt]");
				my $new_annot = join(';', ${$seq_annotation{$annotation_geneN[$i]}{'annotation'}}[$index],$annotation_ary[$cnt]);
				${$seq_annotation{$annotation_geneN[$i]}{'annotation'}}[$index]=$new_annot;
				
			    }
			    else{#if certain range not defined, we push new array in.
				push(@{$seq_annotation{$annotation_geneN[$i]}{'range'}},$range_ary[$cnt]);
				push(@{$seq_annotation{$annotation_geneN[$i]}{'annotation'}}, $annotation_ary[$cnt]);
			    }
														    
							      
			}

		    }
		}
	
	    }
	    
	    foreach my $k(keys %seq_annotation){
		print OFH "%\t$k\n";
		for my $i(0..$#{$seq_annotation{$k}{'range'}}){
		    print OFH "\t${$seq_annotation{$k}{'range'}}[$i]\t${$seq_annotation{$k}{'annotation'}}[$i]\n";
		}
	    }
	    close(OFH);
	}
	
	
    }

    if(defined($q->param("structure"))&&$q->param("structure")){
    ###########################################################
    #structure file is uploaded
	$struct_nm = $q->param("structure");
	
	my @tmp = split(/\/|\\/,$struct_nm);
	$struct_nm = $tmp[$#tmp];
	
	my $chainID = "";
	if(defined($q->param("chain"))&&$q->param("chain")){
	    $chainID = $q->param("chain");
	}
	$struct_nm =~ s/(\.pdb)$//g;
	

	$upload_fhd = $q->upload("structure");
	(defined $upload_fhd) || return ("File handle not defined");
	 
	open(OF, ">$jobdir/$struct_nm.pdb") || return "Cno:$jobdir/$struct_nm.pdb:$!";
	undef $/;
	print OF <$upload_fhd>;
	$/ = "\n";
	close(OF);

	if($chainID ne ""){
	    
	    $structure_f = "$jobdir/$struct_nm.pdb";
	    $struct_nm .= uc($chainID);
	    my $structure_chain_f = "$jobdir/$struct_nm";
	    $structure_chain_f .= ".pdb";
	    my $cmd = "$pdb_extr_chain $structure_f $chainID > $structure_chain_f";
	    system($cmd)&&return "error running $cmd:$!";
	    $structure_f = $structure_chain_f;
	}
	else{
	    $structure_f = "$jobdir/$struct_nm.pdb";
	}

	
    }
    if(defined($q->param("method")) && $q->param("method")){
	$method = $q->param("method");

    }
    
    return('',$qry_nm,$in_fasta,$fasta_fn,$method,
	   $cube,$in_group,$aligned,$similarity_ckbox,
	   \@geneList, $gene_nm_file,
	   $annotation_fileN,\%seq_annotation,$structure_f, $struct_nm);

}

sub getPngFile(@){
    my($resi_count,$png_root, $score, $range) = @_;
    my $f_counter = int($resi_count/$range);
    my @pngfiles = ();
    my $command;
    
    for my $i(0..$f_counter){
	my $frm = ($i*$range)+1;
	my $to = ($i+1)*$range;
	
	if($to > $resi_count){
	    $to = $resi_count;
	}
	$command = "java -jar $seqReport $score $png_root.$frm\_$to $frm $to";
	

	push(@pngfiles,"$png_root.$frm\_$to.png");
	
	system($command) && return "Error Running $command:$!";
    }
    
    return ("",\@pngfiles);

    
}



sub getHtmlHeader(@){
    my ($jmol_header) = @_;
    my $html="";

    
    $html .= "Content-type: text/html\n\n";
    $html .= "<html>\n";
    $html .= "<head>\n";
    if($jmol_header){
	$html .= "<script type=\"text/javascript\" src=\"$jmol_folder/Jmol.js\"></script>\n";
    }
    $html .= "<style type=\"text/css\">\n";
    $html .= ".exceltable\{\n";
    $html .= "\tword-break:break-all\;\n";
    $html .= "\tfont-family:sans-serif\;\n";
    $html .= "\tfont-size:10pt\;\n";
    $html .= "\}\n";
    $html .= "</style>\n";
    $html .= "<body>\n";
    $html .= "<table width=\"800\"  border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\">";

    $html .= "<tr><td> \n";
    $html .= "<br><table width = \"720\" border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" class=\"exceltable\">\n";

    $html .= "<tr><td>\n";
    $html .= "The results may also be accessed later using this url:<br>";
    $html .= "<a href = \"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/cube/Specs.cgi?jobID=$jobID\" target=\"new\">";
    $html .= "http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/cube/Specs.cgi?jobID=$jobID</a>\n";
    $html .= "</td></tr>\n";
    $html .= "<tr><td>\&nbsp;</td></tr>\n";

    $html .= "<tr><td>\n";
    $html .= "<img width=\"430\" src=\"http://epsf.bmad.bii.a-star.edu.sg/images/cons_legend.png\">";
    $html .= "</td></tr>\n";
    
    $html .= "</table></td></tr>\n";
    $html .= "<tr><td>\&nbsp;</td></tr>\n";

    return("",$html);

}

sub getHtmlBottom(){

    my $html="";
  
    $html .= "</table>\n</body>\n</html>";

    return("",$html);

}

sub getHtmlBody(@){
    my $html="";
    my @downloading = @_;
    
    $html .= "<tr><td>";
    $html .= "<table width = \"720\" border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\">\n";
    $html .= "<tr><td> Downloads:\n";
    $html .= "<ul>\n";
   
    foreach my $elem(@downloading){
	
	$html .= "<tr>\n";
	
	$html .= "<td>\n";
	if(ref($elem) eq "ARRAY"){
	    
	    foreach my $png(@{$elem}){
		my @tmp = split(/\./, $png);
		(my $from, my $to) = split(/_/, $tmp[$#tmp-1]);
		$html .= "<br>\nFrom $from to $to<br>\n";
		$html .= "<img src=\"./showImg.cgi?params=$png\" align=\"center\">\n";
		
	    }
	    $html .= "</td></tr>\n";
	}
	else{
	    if($elem =~ /(xls)$|(score)$|(zip)$/){
		#$html .= "<tr><td>\n<a href=\"../struct_server/download.cgi?ID=$elem\">";
		#$html .= "<tr><td> Downloads:\n";
		#$html .= "<ul>\n";
		
		if($elem =~ /(xls)$/){
            
		    #$html .= "<li><a href=\"../struct_server/download.cgi?ID=$elem\">output in excel format</a></li>\n";
		    $html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/struct_server/download.cgi?ID=$elem\">output in excel format</a></li>\n";
		}
		if($elem =~ /(score)$/){
		    #$html .= "<li><a href=\"../struct_server/download.cgi?ID=$elem\">download score file</a></li>\n";
		    $html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/struct_server/download.cgi?ID=$elem\">download score file</a></li>\n";
		}
		#if($elem =~ /(fasta)$/){
		    #my @tmp = split(/\//, $elem);
		    #my $fnm = $tmp[$#tmp];
		    #$fnm =~ s/(.fasta)$//g;
		    #$html .= "download sequence file for $fnm</a>";
		#}
		if($elem =~ /(zip)$/ && -e $elem){ #when user upload a sequence file $elem file not exist
		   
		    
		    if($elem =~ /(\d+\.zip)$/){
		    
			$html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/".
			    "struct_server/download.cgi?ID=$elem\">directory</a></li>\n";
		    }
		    elsif($elem =~ /\.afa/){
			$html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/struct_server/download.cgi?ID=$elem\">the alignements(sorted by species)</a></li>\n";
		    }
		    elsif($elem =~ /\.pse/){
			$html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/struct_server/download.cgi?ID=$elem\">pymol session file</a></li>\n";
		    }
		    elsif($elem =~ /\_specs.py/){
			$html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/struct_server/download.cgi?ID=$elem\">chimera session file for specialization</a></li>\n";
		    }
		    elsif($elem =~ /\_cons.py/){
			$html .= "<li><a href=\"http://epsf.bmad.bii.a-star.edu.sg/cgi-bin/struct_server/download.cgi?ID=$elem\">chimera session file for conservation</a></li>\n";
		    }

		}
	    }
	    else{
		$html .= "<tr><td>\n$elem";
	    }
	    
	    
	    #$html .= "</td>\n</tr>\n";

	}
	

    }
    $html .= "</td>\n</tr>\n";
    $html .= "</table>";
    
    return("",$html);
}

sub getHtmlSpreadsheet(@){
    my ($excel_file,$gene_num, $annot_num) = @_;
    my $html = "";
    my $parser   = Spreadsheet::ParseExcel->new();
    my $workbook = $parser->parse($excel_file);
    
    
    if ( !defined $workbook ) {
        return ($parser->error() . $excel_file);
    }
    $html .= "<tr><td align=\"center\"><div align=\"center\" style=\"overflow:auto; width:720px; height: 500px;\">";
    $html .= "<table width = \"720\" border=\"1\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" class=\"exceltable\">\n";
    
    for my $worksheet ( $workbook->worksheets() ) {

        my ( $row_min, $row_max ) = $worksheet->row_range();
        my ( $col_min, $col_max ) = $worksheet->col_range();
	my ($col, $row, $cell,$format,$bgcolor,$value,$bgcolor_rgb, $colspan);
	
	
	for $row ( $row_min .. $row_max ) {

		$html .= "<tr>\n";

            for $col ( $col_min .. ($col_max -7)) {
		$cell = $worksheet->get_cell( $row, $col );
                
		if($cell){
		    $format = $cell->get_format();
		    $bgcolor = ${$format->{Fill}}[1];
		    $value = $cell->value();
		    $bgcolor_rgb = $parser->ColorIdxToRGB($bgcolor);
		    if($value !~ /(CONSERVATION|SPECIFICITY|REPRESENTATIVE SEQUENCES)|(ANNOTATION)/){
			
			if($value ne "" ){
			    if($value =~ /(alm|gaps|pdb_id|pdb_aa)/){
			    
				$html .= "<td rowspan = \"2\" width=\"80\" bgcolor=\"\#$bgcolor_rgb\">$value</td>\n";
			    }
			    elsif($value =~ /^insert/){
				my $num_colspan = $col_max-7;
				$html .= "<td colspan = \"$num_colspan\" width=\"80\" bgcolor=\"\#$bgcolor_rgb\"><font size=\"0.5\">$value</font></td>\n";
			    }
			    else{
				$html .= "<td width=\"80\" bgcolor=\"\#$bgcolor_rgb\"><font size=\"0.5\">$value</font></td>\n";
			    }
			}
			#elsif($value eq "" && $row eq 1){
			    #$html .= "<td width=\"80\" bgcolor=\"\#$bgcolor_rgb\">\&nbsp\;</td>\n";
			#}
		
		    }
		    else{
			($value =~ /(CONSERVATION)/) && ($colspan = $gene_num+1);
			($value =~ /(SPECIFICITY)/) && ($colspan = 2);#specificity is always occupy two columns
			($value =~ /(REPRESENTATIVE SEQUENCES)/) && ($colspan = $gene_num*2);
			($value =~ /(ANNOTATION)/)&&($colspan = $annot_num);
			$html .= "<td colspan = \"$colspan\" align=\"center\" bgcolor=\"\#$bgcolor_rgb\"><font size=\"1\">$value</font></td>\n";
		    }
		}
	
		
	    }
	    
		$html .= "</tr>\n";

	}
	
    }
    $html .= "</table></div></td></tr>\n";

    return ("", $html);
}
sub getHtmlJmol(@){
    my($jdir,$pyscript) = @_;
    my ($line,$loading);
    my %color=();
    my %specificity = ();
    my %conservation = ();
    my $html = "";
    
    open(FH, "<$pyscript") || return("Cno:$pyscript");
    while($line = <FH>){
	chomp($line);
	
	my $new_color_scheme = "";
	if($line =~ /^(load)/){
	    my @tmp = split(/\s+/, $line);
	    chop($tmp[1]);
	    $loading = $tmp[1];
	    
	}
	elsif($line =~ /^(set_color)/){
	    my @ele_color;
	    my $color_scheme;
	    my @tmp = split(/=/, $line);

	    my $color_name = substr($tmp[0],10);
	    $color_name =~ s/\s+//g;

	    $color_scheme = $tmp[1];
	    $color_scheme =~ s/\[|\]|\s+//g;

	    @ele_color = split(",",$color_scheme);
	    $new_color_scheme ="\[";
	    for my $i(0..$#ele_color){
		$ele_color[$i] = $ele_color[$i]*255;
	    }
	    for my $i(0..$#ele_color){
		if($i != $#ele_color){
		    $new_color_scheme .= "$ele_color[$i], ";
		}
		else{
		    $new_color_scheme .= "$ele_color[$i]\]";
		}
	    }
	    $color{$color_name}=$new_color_scheme;
	  
	}
	elsif($line =~ /^(color)\s+[a-z]+\d+/){
	    my $residue;
	    my @tmp = split(/,/, $line);
	    my $residue_color = substr($tmp[0],6);
	    
	    if($line =~ /(specificity)/){
		$residue = substr($tmp[1],22);
		$residue =~ s/\s+//g;
		$specificity{$residue} = $residue_color;
	    }
	    elsif($line =~ /(conservation)/){
		$residue = substr($tmp[1],23);
		$residue =~ s/\s+//g;
		$conservation{$residue} = $residue_color;
	    }
	}
	
    }
    close(FH);

    $html .= "<tr><td>";
    $html .= "<table width = \"720\" border=\"1\" align=\"center\" cellpadding=\"1\" cellspacing=\"1\">\n";
    $html .= "<tr>\n";
    $html .= Jmolscript(\%color,\%conservation,$loading,"conservation");
    $html .= Jmolscript(\%color,\%specificity,$loading,"specificity");
    $html .= "</tr>\n";
    $html .= "</table>\n";
    $html .= "</td>\n";
    $html .= "</tr>\n";
    $html .= "<tr><td>\&nbsp;</td></tr>\n";
    return("",$html);
    
}

sub Jmolscript(@){
    my($clr_ref,$scheme_ref,$loading_f,$con_or_spec) = @_;
    my $html_script = "";

    $html_script .= "<td>\n";
    
    
    $html_script .= "<script>\n";
    $html_script .= "jmolHtml(\"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\");\n";
    $html_script .= "jmolHtml(\"$con_or_spec\");\n";
    $html_script .= "jmolInitialize\(\"$jmol_folder\"\);\n";
    $html_script .= "jmolSetAppletColor\(\"white\"\);\n";
    $html_script .= "jmolApplet\(350,\n";
    
    
    $html_script .= "\"load\" +\n";
    $html_script .= "\"\\\"http:\/\/epsf.bmad.bii.a-star.edu.sg\/cgi-bin\/struct_server\/download.cgi?ID=$loading_f\\\";\"+\n";
    
    for my $resi(keys %{$scheme_ref}){
	$html_script .= "\"select $resi;\" + \n";
	$html_script .= "\"color ${$clr_ref}{${$scheme_ref}{$resi}};\" + \n";
    }
    $html_script .= "\"select ALL;\" +\n";
    $html_script .= "\"set frank off;\" +\n";
    $html_script .= "\"spacefill off;\" +\n";
    $html_script .= "\"wireframe off;\" +\n";
    $html_script .= "\"cartoon;\" +\n";
    $html_script .= "\"trace 40;\"\)\n";
    $html_script .= "</script>\n";
    
    $html_script .= "<script>\n";
    $html_script .= "jmolHtml(\"\&nbsp;\&nbsp;\");\n";
    #$html_script .= "jmolHtml(\"Conversation\");\n";
    $html_script .= "jmolRadioGroup(\n";
    $html_script .= "[[\"select ALL; cartoon ONLY; trace 40;\", \"cartoon\", \"checked\"],\n";
    $html_script .= "[\"select ALL; backbone ONLY; backbone 0.5;\", \"backbone\"],\n";
    $html_script .= "[\"select ALL; rocket ONLY;\", \"rocket\"]\n";
    $html_script .= "]);\n";
    $html_script .= "</script>";
    
    $html_script .= "</form>\n";
    $html_script .= "</td>\n";

    return($html_script);
    
}
sub runProfile(@){
    my ($nmList_ref,$profile)=@_;
    my $cmd;
    my ($in1,$in2,$tmp_profile);

    $tmp_profile = "$jobdir/tmp_";
    

    $in1 = shift(@$nmList_ref);
    $in2 = shift(@$nmList_ref);
    $tmp_profile .= "$in1\_$in2";
    $cmd = "$muscle -profile -in1 $jobdir/$in1.afa -in2 $jobdir/$in2.afa -out $tmp_profile.afa";
   
    system($cmd) && return("Error running $cmd: $!");
   
    while(@$nmList_ref){
	$in1 = $tmp_profile;
	$in2 = shift(@$nmList_ref);
	
	$tmp_profile .= "_$in2";
	$cmd = "$muscle -profile -in1 $in1.afa -in2 $jobdir/$in2.afa -out $tmp_profile.afa";
	
	system($cmd);
    }
    
    `cp $tmp_profile.afa $profile`;
    
    return("");

}

sub generateCmdFile(@){
    my ($cmd_tmp_file, $cmd_file, $almt, $group, $outnm,$pdb,$structure_nm,$similarity) = @_;
    
    open(IF,"<$cmd_tmp_cub")||return("Cno:$cmd_tmp_cub");
    undef $/;
    my $prms_string = <IF>;
    $/ = "\n";
    close IF;

	
    $prms_string =~ s/almtname/$almt/;
    $prms_string =~ s/groups/$group/;
    $prms_string=~ s/outname/$outnm/;
    if($pdb){
	$prms_string =~ s/!pdbname/$pdb/;
	$prms_string =~ s/!struct_n/$structure_nm/;
    }
    if($similarity){
	$prms_string =~ s/!exchangeability/exchangeability/;
    }
    
    open(OF, ">$cmd_file")||return("Cno:$jobdir/cmd");
    print OF $prms_string;
    close(OF);
    
    return("");

}

sub addAnnot(@){
    my($score_file,$annot_ref,$alm_msf) = @_;
    my $score_annot_file = $score_file . ".annot";
    my $tmp_file = $score_file . ".tmp";
    open(MSF, "<$alm_msf")||return("Cno:$alm_msf");
    while(<MSF>){
	last if(/\/\//);
    }
    my %sequence = ();
    my @names = ();
    do {
	if ( /\w/ ) {
	    my @aux = split;
	    my $name = $aux[0];
	    my $aux_str = join ('', @aux[1 .. $#aux] );
	    if($name =~ /(HOM_SAP)/){#human genes only
		if ( defined $sequence{$name} ) {
		    $sequence{$name} .= $aux_str;
		} else {
		    push @names, $name;
		    $sequence{$name}  = $aux_str;
		}
	    }
		
	} 
    } while ( <MSF>);

    # turn the msf into a table (first index= sequence, 2bd index= position
    my $seq = 0;
    my (%array,%counter,%seqno);
    my @annot_names = ();
   
    
    foreach my $name ( @names ) {
	
	my @aux = split '', $sequence{$name};
	foreach my $pos ( 0 .. $#aux ) {
	    $array{$name}[$pos] = $aux[$pos];
	    if ( $aux[$pos] !~ /[\.\-]/ ) {
		(defined  $counter{$name}) || ($counter{$name} = 0);
		$counter{$name} ++;
		$seqno{$name}[$pos] = $counter{$name};
	    } else {
		$seqno{$name}[$pos] = "-";
	    }
	}
	$seq++;
    
    }
    
    foreach my $g(keys %$annot_ref){
	my $g_seqno = "HOM_SAP_$g";
	

	if(defined($seqno{$g_seqno})){
	#foreach my $k(keys %seqno){
	    #if($k =~ /($g)/i){
		push( @annot_names,$g_seqno);
		for my $i(0..$#{$annot_ref->{$g}{'range'}}){
	
		    for my $j(0..$#{$seqno{$g_seqno}}){
		    
			if($seqno{$g_seqno}[$j] eq $annot_ref->{$g}{'range'}[$i]){
			    $seqno{$g_seqno}[$j]= $annot_ref->{$g}{'annotation'}[$i];
			    last;
			}
		       
		    }
		    #for my $j(0..$#{$seqno{$k}}){
		    
			#if($seqno{$k}[$j] eq $annot_ref->{$g}{'range'}[$i]){
			    #$seqno{$k}[$j]= $annot_ref->{$g}{'annotation'}[$i];
			    #last;
			#}
		       
		    #}
		}
	    }
	#}
	
	
    }
    my $nm_str = "";
    my $annot_str = "";
    if(@annot_names){
	#dieproc(join("",@annot_names));
	$nm_str = join("\t",@annot_names);
	
	open(OFH,">$tmp_file")||return("Cno:$tmp_file");
	print OFH "$nm_str\n";
	for my $i(0..$#{$seqno{$annot_names[0]}}){ #here random chose $annot_name[0],since all seq are the same length with gappes
	    
	    for my $j(0..$#annot_names){
		
		if($j ne $#annot_names){
		    if($seqno{$annot_names[$j]}[$i] =~ /\D/){
			$annot_str .= $seqno{$annot_names[$j]}[$i] . "\t";
		    }
		    else{
			$annot_str .= "-\t";
		    }
		}
		else{
		    if($seqno{$annot_names[$j]}[$i] =~ /\D/){
			$annot_str .= $seqno{$annot_names[$j]}[$i] . "\n";
		    }
		    else{
			$annot_str .= "-\n";
		    }
		}
	    }
	}
	print OFH $annot_str;
	close(OFH);
	`pr -m -t -s $score_file $tmp_file > $score_annot_file`;
    }
    #if(-e $score_annot_file){ 
	return ("", $score_annot_file);
    #}
    #else{
	#return ("", "");
    #}
}

sub deleteGap(@){
    my ($file) = @_;
    my (@aux,@aux_previous);
    my $cnt_begin = 0;
    my $cnt_end = 0;
    my $counter = 0;
    my $pos_column = 0;
    my $number_of_groups = 0;
    my $file_lessgap = "$file.lessgap";
    open(FH, "<$file") || return("Cno:$file");
    open(OFH,">$file_lessgap") || return("Cno:$file_lessgap");
    while(<FH>){
	my $flag = 0;
	
	next if ( !/\S/);
	if ( /\%/ ){
	    @aux = split;
	    shift @aux;
	    
	    while ($pos_column < @aux){
		if($aux[$pos_column] =~ /pos_in/){
		    $number_of_groups++;
		}
		$pos_column++;
	    }
	    print OFH "%\t";
	    print OFH join("\t",@aux);
	    print OFH "\n";
	}
	else{
	    chomp;
	    if($aux[0] !~ /(almt)/){
		@aux_previous = @aux;
	    }
	    @aux = split;
	    
	    for my $i((4+$number_of_groups)..$#aux){#4:alm,gaps,rvet,disc,dets_in, 
                                                    #here to check if the gaps in columns (4+$number_of_groups) to the last column
		if($aux[$i] !~ /\.|\-/){
		    
		    $flag = 1;
		    last;
		}
		
	    }
	    if(!$flag){
		$counter++;
		($cnt_begin) || ($cnt_begin=$aux[0]);
	
	    }
	    else{
		$cnt_end = $cnt_begin + $counter - 1;
		if(@aux_previous && $counter != 0){
		    if($cnt_begin != $cnt_end){
			$aux_previous[0] = "$cnt_begin-$cnt_end";
		    }
		    print OFH " \t";
		    print OFH join("\t",@aux_previous);
		    print OFH "\n";
		}
		print OFH " \t";
		print OFH join("\t",@aux);
		print OFH "\n";
		$counter = 0;
		$cnt_begin = 0;
		$cnt_end = 0;		
	    }
	}
	
    }
    close(OFH);
    close(FH);
    return("",$file_lessgap);
}


sub dieproc(@){
    my ($msg,$msg_for_author,$ml) = @_;
    my $err_str = "";
    if($ml){
	mailme("SPECS",$msg_for_author);
    }
    $err_str .= "Content-Type:text/html\n\n";
    $err_str .= "<head>\n";
    $err_str .= "<style type=\"text/css\">\n";
    $err_str .= "\.style \{\n";
    $err_str .= "font-family: \"Courier New\"\;\n";
    $err_str .= "font-size: medium\;\n";
    $err_str .= "\}\n</style>\n";
    $err_str .= "</head> \n<body>\n";
    $err_str .= "<table width=\"750\"  border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\">\n";
    $err_str .= "<tr>\n";
    $err_str .= "<td width=\"750\"><img src=\"http://epsf.bmad.bii.a-star.edu.sg/Image/s_body_top2.jpg\">\n";
    $err_str .= "</td>\n";
    $err_str .= "</tr>\n";		
    $err_str .= "<tr>\n";
    $err_str .= "<td width=\"750\">";
    $err_str .= "<table width = \"100%\" border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" background=\"http://epsf.bmad.bii.a-star.edu.sg/Image/s_body_bg2.jpg\">\n";
    $err_str .= " <tr><td>\&nbsp\;</td><td>\&nbsp\;</td>\n";
    $err_str .= "<td>\n";
    $err_str .= "$msg\n";
    $err_str .= "</td></tr>\n";
    $err_str .= "</table>\n";
    $err_str .= "</td>\n";
    $err_str .= "</tr>\n";
    $err_str .= "<tr>\n";
    $err_str .= "<td width=\"750\">\n";
    $err_str .= "<img src=\"http://epsf.bmad.bii.a-star.edu.sg/Image/s_body_bottom2.jpg\">\n";	
    $err_str .= "</td>\n";
    $err_str .= "</tr>\n";
    $err_str .= "</table>\n";
    $err_str .= "</body></html>\n";
    
    `echo \"$err_str\" > $htmlf`;
    exit;
    #} 
    #else{
	#mailme("SPECS",$msg_for_author);
	#$err_str .= "Content-Type:text/html\n\n";
	#$err_str .= "$msg\n";
    
	#`echo \"$err_str\" > $htmlf`;
	
	#exit;
    #}
	    
}
