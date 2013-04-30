use strict;

########################################################################
#CUBE
#######################################################################


sub add_annotation    (@);
sub delete_gapped_pos (@);
sub generate_cmd_file (@);


sub specialization (@){

    my ($jobID, $jobdir,  $ref_seq_name, $alignment_file, $group_file, $score_method,
	$seq_not_aligned,  $seq_annotation_ref, $name_resolution_file,
	$structure, $struct_name, $chainID,  $dssp,
	$cube, $cube_cmd_template, $hc2xls,  $seqReportEE, $hc2pml, $pymol, $zip, $jmol_folder) = @_;

    my $cmd_file = "$jobdir/cmd"; #cmd file for hyper cube
    my $htmlf    = "$jobdir/display.html";
    my $url;
    my $gene_notfound=0;
    my ($almt, $group,$outnm,$xls_fnm, $almt_f);
    my $pdbf = 0;
    my $struct_nm = 0;
    my @fnm_seq = ();
    my @fnm_seq_alt =  ();
    my $stdout = "$jobdir/cube.stdout";
    my $stderr = "$jobdir/cube.stderr";
    my ($cmd, $errmsg);

    my $number_of_annotated_seqs;
	

    my  @lines =  split "\n", `grep "name" $group_file`;
    my  @group_names = ();
    foreach my $line (@lines) {
	my @aux = split " ", $line;
	push @group_names, $aux[1];
    }
    my $number_of_groups = int  @group_names;

    ($number_of_groups > 1) ||  html_die ("Malformatted group file." );

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
    # lines for the cmd file for cube a.k.a. hyper_c program
    $outnm    = "$jobdir/out";
    ($errmsg) = generate_cmd_file($cube_cmd_template, $cmd_file, 
				  $alignment_file, $group_file, $outnm,
				  $structure, $struct_name, $score_method);
    ($errmsg eq "") || html_die($errmsg);
    
    #############################################
    # the action happens here:
    $cmd = "$cube $cmd_file  1> $stdout 2> $stderr";
    if (system $cmd) {

	# cube itself will check if the structure can be found in the alignment
	if(`grep '^Structure' $stderr`){
	    html_die ("structure $struct_name not found in the alignment file");

	} else {
	    my $ret = `grep 'Unrecognized amino acid code' $stdout`;
	    $ret && html_die("Error parsing $structure:\n$ret\n");
	}

	html_die ( "$cmd\n$stdout\n$stderr\n");
    }

    ###############################################
    #generate png with the conservation mapped on the sequence
    my $score_file          = "$jobdir/out.score";
    my $png_input            = "$jobdir/png_input";
    $cmd = "awk \'\$1 \!= \"\%\"  && \$4 \!= \".\"   \{print \$3 \"  \" \$4 \"   \" \$5\}\' $score_file > $png_input"; 
    (system $cmd) && html_die ("<pre> $cmd </pre>");
    

    #############################################
    # add annotation, if provided
    my $score_annotated;
    my $input_for_xls       = $score_file;
    if ( $seq_annotation_ref) {
	$input_for_xls  = add_annotation ($score_file, $seq_annotation_ref, $name_resolution_file, $alignment_file);
    } 

    #############################################
    # generate xls
    my $xls = "$jobdir/out.xls";
    $cmd = "$hc2xls  $input_for_xls  $xls";
    (system $cmd) && ($xls="");

    #############################################
    # generate pymol session
    my $pymol_session = "";

    if($structure){
	    
	my $pymolscript = "$jobdir/out.pml";
	$pymol_session  = $pymolscript;
	$pymol_session  =~ s/pml/pse/;

	my $cmd = "$hc2pml $score_file $structure $pymolscript -c $chainID";
	if ( @group_names < 3 ) {
	    $cmd .= "  -g @group_names "; # determinants for the groups 
	}
	(system $cmd) &&  ($pymol_session = "");
	
	$cmd = "$pymol -qc -u $pymolscript > /dev/null";
	system($cmd)  &&  ($pymol_session = "");

	if ( $pymol_session ) {

	    # on sucess the returned $pymol_session  will be $pymol_session.".zip"
	    # on failure it will be ""
	    $pymol_session = zip_file ($zip,$pymol_session);
	}

    }  

    #############################################
    #zip the whole directory
    my $dirzipfile = zip_directory($zip, $jobdir);
	

    #############################################
    #############################################
    # html production
    #############################################

    #############################################
    #generate header
    my $html_header;
    my $java_script = "";
    $structure &&  ($java_script = "$jmol_folder/Jmol.js");
    $html_header = html_generic_head($java_script);
    

    #############################################
    #generate body
    my $html_body=  "";
	
    $html_body .= html_specialization_body_top($jobID, $ref_seq_name);

    if($structure){
	my ($html_pyml,$html_chi_specs, $html_chi_cons);

	$html_body .= html_generic_downloadables ($xls,  $score_file, $dirzipfile,
						  $pymol_session, "", "");
	# jmol just too foogly
	#$html_body .= html_jmol ($jobdir, $jmol_folder, $pymolscript);

    } else{
	$html_body .= html_generic_downloadables ($xls,  $score_file, $dirzipfile);
    }

    #################################################
    #display spreadsheet as html
    #################################################
    my $html_spreadsheet;
    ($errmsg, $html_spreadsheet) = html_spreadsheet_cube($xls, $number_of_groups, $number_of_annotated_seqs);
    ($errmsg eq "") || html_die($errmsg);
    $html_body      .= $html_spreadsheet;
    
    #################################################
    #generate bottom
    #################################################
    my $html_bottom = html_generic_body_bottom();
    
    #################################################
    #
    print $html_header.$html_body.$html_bottom;

    open(FH, ">$htmlf")||html_die("cno:$htmlf","cno:$htmlf",1);
    print FH "$html_header$html_body$html_bottom";
    close(FH);
    
}



##################################################################################################
sub generate_cmd_file(@){

    my ($cube_cmd_template, $cmd_file, $alignment_file, $group_file, $outnm,
	$pdbf, $struct_nm, $similarity)= @_;
    
    open(IF,"<$cube_cmd_template")||return("Cno:$cube_cmd_template");
    undef $/;
    my $prms_string = <IF>;
    $/ = "\n";
    close IF;

    $prms_string =~ s/almtname/almtname  $alignment_file/;
    $prms_string =~ s/groups/groups    $group_file/;
    $prms_string =~ s/outname/outname   $outnm/;

    
    if($pdbf){
	$prms_string =~ s/!pdb_file/pdb_file  $pdbf/;
	$prms_string =~ s/!pdb_name/pdb_name  pdb_$struct_nm/;
    }
    if($similarity){
	$prms_string =~ s/!exchangeability/exchangeability/;
    }
    
    open(OF, ">$cmd_file") || return  "Cno: $cmd_file";
    print OF $prms_string;
    close(OF);
    
    return "";

}


##################################################################################################
sub delete_gapped_pos (@) {

    my ($file) = @_;
    my (@aux,@aux_previous);
    my $cnt_begin = 0;
    my $cnt_end = 0;
    my $counter = 0;
    my $pos_column = 0;
    my $number_of_groups = 0;
    my $file_lessgap = "$file.no_gaps_in_refseq";

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

return 1;
