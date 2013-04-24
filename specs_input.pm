use strict;
sub process_annotation (@);

##############################################################################
sub process_input_params(@){


    my ($q,$jobdir) = @_;
    my $job_type;
    my @input_seq_files = ();
    my $similarity_ckbox = 0;
    #default method for specs is rvet
    my $method = "rvet";


    if ( ! defined $q->param("fnm") ) {
	html_die ("Please provide sequence file(s) for the analysis.");
    }
    my @upload_filehandles = $q->param("fnm");
    my $size = int @upload_filehandles;

    if( $size == 0){
        html_die ("Please provide sequence file(s) for the analysis.");
    } elsif  ($size > 1) {
	#specs
	$job_type = SPECIALIZATION_WITH_SEQS_PROVIDED;;
    } elsif  ($size) {
	#cube with sequence as input
	$job_type = CONSERVATION;
    }

    my ($upload_fhd,  $in_fasta, $in_group, $structure_name);
    my @geneList = ();
    #my $mthd = 0;
    my $ref_seq_name = "";
    my $gene_nm_file    = 0;
    my $seq_not_aligned = 0;
    my $structure_f     = 0;
    
    if( defined($q->param("similarity")) && $q->param("similarity")){
	$similarity_ckbox = $q->param("similarity");
    }
	
    if($job_type == CONSERVATION){ #specs requires a reference sequence
	$ref_seq_name = $q->param("qry_nm");
    }

    if (defined($q->param("ckb")) && $q->param("ckb")) {
	$seq_not_aligned = 1;
    }
    

    for my $upload_fhd ( @upload_filehandles) {
	
	my @tmp = split(/\\/, $upload_fhd);
	my $filename = pop @tmp;
	my $in_fasta = "$jobdir/$filename";
	
	open(OF, ">$in_fasta") || return "Cno: $in_fasta:$!\n";
	undef $/;
	print OF <$upload_fhd>;
	$/ = "\n";
	close(OF);

	push @input_seq_files, $in_fasta;
    }
	
    if(defined($q->param("method")) && $q->param("method")){
	$method = $q->param("method");
    }


    ###########################################################
    # upload the structure file (if provided) 
    my $chainID = "";
    if(defined($q->param("structure"))&&$q->param("structure")){
	$upload_fhd = $q->upload("structure");
	(defined $upload_fhd) || return ("Stucture file not uploaded.");
	 
	$structure_name = $q->param("structure");
	my @tmp = split(/\/|\\/,$structure_name);
	$structure_name = $tmp[$#tmp];
	
	if(defined($q->param("chain"))&&$q->param("chain")){
	    $chainID = $q->param("chain");
	}
	$structure_name =~ s/(\.pdb)$//g;
	
	open(OF, ">$jobdir/$structure_name.pdb") || return "Cno: $jobdir/$structure_name.pdb:$!";
	undef $/;
	print OF <$upload_fhd>;
	$/ = "\n";
	close(OF);
	
    }


    ###########################################################
    # read in the annotation (if provided) 
    my $seq_annotation_ref   = 0;
    if ( defined($q->param("anno")) && $q->param("anno")) {
	$seq_annotation_ref = process_annotation ($jobdir, $q);
    } 
    
    return('', $ref_seq_name, \@input_seq_files, $method,
	   $job_type, $seq_not_aligned, \@geneList, $gene_nm_file,
	   $seq_annotation_ref, $structure_name, $chainID);

}

##############################################################################
##############################################################################
##############################################################################
sub process_input_data (@) {

    my ($jobdir, $job_type, $input_seq_files_ref, $seq_not_aligned, $ref_seq_name,  
	$structure_name, $chainID, $pdb_extract_chain, $pdb2seq, $fasta_rename, $msf2afa, $muscle, $afa2msf) = @_;
    my $errmsg = "";
    
    my @input_seq_files = @{$input_seq_files_ref};
    my @alignment_files = ();
    my $alignment_file;
    my $cmd;
    my $group_name    = "";
    my %group_members = ();

    defined($ref_seq_name) || ($ref_seq_name="");

    if ($ref_seq_name) {
	my $refseq_found    = "";
	
	for my $input_seq_file (@input_seq_files ) {
	    # check whether the reference sequence appears in the alignment
	    $refseq_found = `grep "Name: $ref_seq_name" $input_seq_file` ||
		`grep  \'>\' $input_seq_file | grep \'$ref_seq_name\'`;
	    $refseq_found  && last;
	}
	if (!$refseq_found) {
	    $errmsg = "The reference name $ref_seq_name does not appear in the alignment file.<br>".
		" Please include the reference sequence, or perhaps check the name spelling";
	    return ($errmsg, "");
	}
    }

    for my $input_seq_file (@input_seq_files ) {

	# do we recognize the format?
	$cmd = "grep \" Name:\" $input_seq_file | head -n1";
	my $first_name_line = `$cmd`;
	my $alignment_format = "";

	if($first_name_line){ # we are assuming the msf format
	    $alignment_format = "MSF";
	} else {
	    $cmd = "grep \">\"  $input_seq_file | head -n1";
	    $first_name_line = `$cmd`;
	    if($first_name_line){
		$alignment_format = "AFA";
	    } else {
		$errmsg = "The alignment format not recognized for $input_seq_file. Check ".
		    " <a href=\"http://eopsf.org/cube/gcg_example.txt\">here (GCG, a.k.a. MSF)</a>".
		    " and  <a href=\"http://eopsf.org/cube/fasta_example.txt\">here (FASTA)</a>" .
		    " for the two formats that the current implementation recognizes.";
		return ($errmsg, "");
	    }
	    # TODO: clean up and simplify names - I think clustalw and such would have already
	    # chooped the names, so we have to worry only about afa files
	    # 1) grep '>' there is fasta_rename.pl in scripts dir -- see specs.cgi header
	    # 2) modify it ouput the original header and the replacement name, ann save that info to jobdir
	    # 3) make sure that the refseq name correponds to the new shortened name



	}

	# if we still don't have the $ref_seq_name take the first one that appears in the alignment
	if ($job_type==CONSERVATION && !$ref_seq_name) {
	    if($alignment_format eq "MSF" ){
		$first_name_line =~ /Name\:\s*(\w+)/;
		(defined $1 && $1) && ($ref_seq_name = $1);
	    } else {
		$first_name_line =~ />\s*(\w+)/;
		(defined $1 && $1) && ($ref_seq_name = $1);
	    } 
	    
	    $ref_seq_name || html_die ("Unspecified error in the input alignment format.");
	    
	}

	# generate new name for the aligned file
	if ( $input_seq_file =~ /(.+)\.(\w+)$/) {
	    my $root = $1;
	    my $ext  = $2;
	    if ($ext eq "afa") {
		$alignment_file = "$root.2.afa";
	    } else {
		$alignment_file = "$root.afa";
	    }
	    if ($job_type!=CONSERVATION) {
		my @tmp     = split '/',  $root;
		$group_name =  pop @tmp;
	    }
	} else {
	    $alignment_file  = "$input_seq_file.afa";
	}


	# if not aligned, align
	if ($seq_not_aligned) {

	    if($alignment_format eq "MSF" ){ #how could this happen ?
		$cmd = "$msf2afa $input_seq_file > $input_seq_file.afa";
		system($cmd) && html_die ("Error running $cmd\n");
		`mv $input_seq_file.afa $input_seq_file`; 
	    }
	    $cmd = "$muscle -in $input_seq_file -out $alignment_file >>  $jobdir/muscle.out 2>&1";
	    my $errlog = `cat $jobdir/muscle.out`;
	    system($cmd) && html_die("Error running $cmd:\n$errlog\n");

	} else { 
	    # afa, turn to msf
	    if($alignment_format eq "AFA" ){
		$alignment_file = $input_seq_file;
	    } else {
		# msf2afa  muscle does not like outputing msf
		$cmd = "$msf2afa  $input_seq_file > $alignment_file";
		system($cmd) && html_die ("error running $cmd\n");
	    }
	}

	push @alignment_files, $alignment_file;

	if ($job_type!=CONSERVATION) {
	    $group_members{$group_name} = `grep '>' $alignment_file | sed 's/>//g'`;
	}
    }

    my $group_file = "";
    if ($job_type!=CONSERVATION) {

	$group_file = "$jobdir/groups";
	open(GFH, ">$group_file") || html_die ("Error writing to a file (?!)");
	for $group_name (keys %group_members) {
	    print  GFH  "name  $group_name\n";
	    print  GFH  $group_members{$group_name};
	    print  GFH  "\n";
	}
	close GFH;
    }

    
    my $log = "";
    $log .= join "\n", @input_seq_files;
    $log .=  "\n";
    $log .= join "\n", @alignment_files;
    $log .=  "\n";
    

    # we want one single file
    if (@alignment_files==1) {
	$alignment_file = $alignment_files[0];

    } else {
	# do profile alignment
	my $prev_aln = "$jobdir/prev.afa";
	my $last_aln = "$jobdir/all.afa";
	`cp $alignment_files[0] $last_aln`;
	$log .=  "cp $alignment_files[0] $last_aln \n";
	for my $aln ( @alignment_files[1 .. $#alignment_files] ) {
	    `mv  $last_aln $prev_aln`;
	    $log .= "mv  $last_aln $prev_aln \n";
	    $cmd  = "$muscle -profile -in1 $prev_aln -in2 $aln  -out $last_aln >>  $jobdir/muscle.out 2>&1";
	    $log .= "$cmd\n";
	    my $errlog = `cat $jobdir/muscle.out`;
	    my $msg = "Error creating profile alignment.\n".
		"Are your sequences aligned? If not, please ".
		"tick the 'My sequences are not aligned' checkbox.\n";
	    system($cmd) && html_die($msg);
	}
	`rm $prev_aln`;
	$alignment_file = $last_aln;
    }

    my $structure_file = "";
    if ($structure_name) {

	my $structure_chain_f;
	$structure_file    = "$jobdir/$structure_name.pdb";

	# are we using the whole PDB file, or just one chain?
	if( $chainID ){
	    $structure_chain_f    = "$jobdir/$structure_name.".uc($chainID).".pdb";
	    my $cmd = "$pdb_extract_chain $structure_file $chainID > $structure_chain_f";
	    system($cmd)&&return "Error running \n$cmd\n$!";

	} else{
	    $structure_chain_f = $structure_file;
	}
	# add the structure sequence to the alignment
	# pdb2seq
	my $seq_file = "$jobdir/$structure_name.seq";
	$cmd = "$pdb2seq $structure_chain_f  pdb_$structure_name >  $seq_file";
	system($cmd) && html_die ("error running $cmd\n");
        # muscle
	$cmd = "$muscle -profile -in1 $alignment_file  -in2 $seq_file -out $jobdir/tmp.afa";
	system($cmd) && html_die ("error running $cmd\n");
	`mv $jobdir/tmp.afa $alignment_file`;
    }

    my $alignment_file_msf = $alignment_file;
    $alignment_file_msf    =~ s/afa$/msf/;
    $cmd = "$afa2msf  $alignment_file > $alignment_file_msf";
    system($cmd) && html_die ("$log\nerror running $cmd\n");
    
 
    return ("", $ref_seq_name, $alignment_file_msf, $group_file, $structure_name, $structure_file);

}
##############################################################################
##############################################################################
##############################################################################
sub process_annotation (@) {

    my ($jobdir, $q) = @_;
    my (@gnm_ary, @range_ary, @inf_ary);
    my $annotation_file_name ="$jobdir/ann.txt";

    my @parameter_names    = $q->param();
    my @annotated_sequence = ();
    my @annotation_range   = ();
    my @annotation_text    = ();
    my %seq_annotation     = ();

    my $log = "@parameter_names\n";

    foreach my $nm (@parameter_names){

	if($nm =~ /^gene_name/){
	    my $tp = $q->param($nm);
	    defined($tp) && $tp  && push(@annotated_sequence, $tp);
			
	} elsif($nm =~ /^range/){
	    my $tp = $q->param($nm);
	    defined($tp) && $tp && push(@annotation_range, $tp);
			
	} elsif($nm =~ /^information/){
	    my $tp = $q->param($nm);
	    defined($tp) && $tp && push(@annotation_text, $tp);

	}
    }
    $log .= "@annotated_sequence\n"."@annotation_range\n"."@annotation_text\n";



    for my $i(0..$#annotated_sequence){
		
	my $seq_name = $annotated_sequence[$i];
	my $range    = $annotation_range[$i];
	my $text     = $annotation_text[$i];
	my $pos;
		
	($seq_name && $range  && $text) || next; # drop the incomplete info
	(defined $seq_annotation{$seq_name}) ||  ($seq_annotation{$seq_name} = ());

	# parse the range
	$range =~ s/\s//g;
	my @fields = split(/,/, $range);
	foreach my $field (@fields){
	    
	    if($field =~ /-/){
		my @tmp = split(/-/,$field);
		(@tmp > 2) && next;
		($tmp[0] =~ /D/) && next;
		($tmp[1] =~ /D/) && next;

		my $start = $tmp[0];
		my $end   = $tmp[1];
		if ( $tmp[0] > $tmp[1]) {
		    $start = $tmp[1];
		    $end   = $tmp[0];
		}

		for $pos ( $start .. $end ){
		    if ( !defined  $seq_annotation{$seq_name}[$pos]) {
			$seq_annotation{$seq_name}[$pos] = $text;
		    } else {
			$seq_annotation{$seq_name}[$pos] .= "\t".$text;
		    }
		}

	    } else {
		($field =~ /D/) && next;
		$pos = $field;
		if ( !defined  $seq_annotation{$seq_name}[$pos]) {
		    $seq_annotation{$seq_name}[$pos] = $text;
		} else {
		    $seq_annotation{$seq_name}[$pos] .= "\t".$text;
		}
	    }
	}
    }


    open(OFH, ">$annotation_file_name") || html_die ("Some weirdness: $annotation_file_name:$!");
    foreach my $seq_name (keys %seq_annotation){
	my $largest_pos = $#{$seq_annotation{$seq_name}};
	for my $i (0 .. $largest_pos) {
	    defined $seq_annotation{$seq_name}[$i] || next;
	    print OFH "$seq_name\t$i\t".$seq_annotation{$seq_name}[$i  ]."\n";
	    
	}
    }
    close(OFH);

    return \%seq_annotation;

}


return 1;
