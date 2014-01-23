use strict;

###################################################
#  CONSERVATION
###################################################

sub add_annotation(@); # in specs_utils.pm

sub conservation (@) {

    my  ($jobID, $jobdir, $ref_seq_name, $alignment_file,  $score_method,
	 $seq_not_aligned,  $seq_annotation_ref, $name_resolution_file, 
	 $structure, $struct_name, $chainID, $structure_single_chain,  $dssp, 
	 $specs, $specs2pml, $specs2excel,  $seqReport, $pymol, $zip) = @_;

    my $input_name_root = delete_extension($alignment_file);
    

    my ($cmd, $errmsg, $specs_cmd_file);
    my $prms_string;
    my $htmlf            = "$jobdir/display.html";
    my $excel_out        = "$input_name_root";
    my $pdbf;
    my $png_input        = "$input_name_root\.$score_method";
    my $png_f            = "$input_name_root";
    my $para_string;
    my $score_f          = "$jobdir/specs_out\.score";


    #############################################
    # run dssp (solvent accessibility):
    my $dssp_file = "";
    if($structure){
	$dssp_file = $structure;
	$dssp_file =~ s/pdb$/dssp/;
	$cmd = "$dssp -i $structure -o $dssp_file";
	(system $cmd) && ($dssp_file="");
    }


    #############################################
    # create the cmd file
    # 
    $prms_string  = "";
    # defaults:
    $prms_string .= "patch_sim_cutoff   0.4\n";
    $prms_string .= "patch_min_length   0.4\n";
    $prms_string .= "sink  0.3  \n";
    $prms_string .= "skip_query \n";
    $prms_string .= "\n";
 
    $prms_string .= "align   $alignment_file\n";
    $prms_string .= "refseq  $ref_seq_name\n";
    $prms_string .= "method  $score_method\n";
    $prms_string .= "\n";
    $prms_string .= "outn  $jobdir/specs_out\n";


    if($structure){
	
	$prms_string .= "pdbf      $jobdir/$structure_single_chain.pdb  \n";
	$prms_string .= "pdbseq    pdb_$structure_single_chain\n";
	$dssp_file  &&  ($prms_string .= "dssp   $dssp_file\n");
	    
    }
    
    $specs_cmd_file = "$jobdir/specs_cmd";

    open(FH, ">$specs_cmd_file") || diehard("specs","Cno:$specs_cmd_file, $!\n");
    undef $/;
    print FH $prms_string;
    $/="\n";
	
    close(FH);

    #############################################
    # run specs
    # 
    my $stdout = "$jobdir/specs.stdout";
    my $stderr = "$jobdir/specs.stderr";

    $cmd = "$specs $specs_cmd_file 1>$stdout 2>$stderr";
    
    if (system $cmd) {
	my $errlog = `cat $stderr`;
	$errlog .= `cat $stdout`;
	html_die("Error running \n$cmd\n$errlog\n");
    }

    if($errmsg = `grep \"Unrecognized amino acid code\" $stdout`){
	chomp($errmsg);
	html_die("$errmsg in the uploaded strucure");
    }
    
    ###############################################
    #generate png with the conservation mapped on the sequence
    $cmd = "awk \'\$1 \!= \"\%\"  && \$4 \!= \".\"   \{print \$3 \"  \" \$4 \"   \" \$5\}\' $score_f > $png_input"; 
    (system $cmd) && html_die ("<pre> $cmd </pre>");
    

    my @resi_cnt = split(/\s/,`wc -l $png_input`);
    my $num_resi = $resi_cnt[0];
    my $range = 400;
    ($errmsg, my $png_ref) = make_conservation_map_png($seqReport, $num_resi, $png_f, $png_input, $range);

    ($errmsg eq "") || html_die("<pre> $errmsg </pre>");
    
    ##############################################
    # add annotation, if provided
    my $score_annotated;
    my $score_file      = "$jobdir/specs_out.score";
    my $input_for_xls   = $score_file;
    if ($seq_annotation_ref) {
	$input_for_xls  = add_annotation ($score_file, $seq_annotation_ref, 
					  $name_resolution_file, $alignment_file);
    } 

    ##############################################
    #generate excel spreadsheet
    $cmd = "$specs2excel $input_for_xls  $input_name_root";

    (system $cmd) && html_die ("<pre>Error running $cmd: $!<pre>");

    $excel_out .= ".xls";

    ##############################################
    #generate pymol session
    my $script = "$jobdir/$ref_seq_name.pml";
    my ($zipfile,$session);
    
    if($structure){

	# check whether chain really exists in this structure
	# otherwise we get nonsense
	my $ret  = `awk '\$1=="ATOM"' $structure | head -n1`;
	my $chainID_in_pdb_file = substr ( $ret,  21, 1);
	
	$cmd = "$specs2pml  $score_method  $score_f  $structure $script ";
	($chainID_in_pdb_file =~ /\w/) && ($cmd .= " $chainID");
	
	system($cmd) && html_die("Error running $cmd:$!");

	$cmd = "$pymol -qc -u $script > /dev/null";
	system($cmd) && html_die("Error running $cmd $!");

	$session = $script;
	(($session =~ s/\.pml$/\.pse/)==1) || 
	    diehard("specs", "Can not construct session name:$cmd");
	$zipfile = "$session.zip";
	$cmd = "$zip -j $zipfile $session > /dev/null";
	
	system($cmd) && ($zipfile="");
    }

    ###########################################################################
    #zip the whole directory
    my $dirzipfile =  zip_directory($zip, $jobdir);

    ###########################################################################
    #display the output

    my ($html_head, $html_top, $html_middle, $html_bottom);

    $html_head   = html_generic_head ();
    $html_top    = html_conservation_body_top ($jobID, $ref_seq_name);
    $html_middle = html_generic_downloadables ($score_f, $excel_out, $zipfile, $dirzipfile,$png_ref, "Conservation map", CONSERVATION);
    $html_bottom = html_generic_body_bottom();

    print $html_head.$html_top.$html_middle.$html_bottom;
    # we'll offer the html page itslef for download
    open(FH,">$htmlf") || diehard("specs","Cno:$htmlf");
    print FH $html_head.$html_top.$html_middle.$html_bottom;
    close(FH);

}

######################################################################################################
######################################################################################################
sub make_conservation_map_png(@){
    my($seqReport, $resi_count,$png_root, $score, $range) = @_;
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
	
	if (system($command)) {
	    $command =~ s/\s+/\n/g;
	    html_die "Error Running $command:$!";
	}
	push(@pngfiles,"$png_root.$frm\_$to.png");
	
    }
    
    return ("",\@pngfiles);

    
}



return 1;
