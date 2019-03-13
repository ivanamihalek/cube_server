use strict;
use warnings FATAL => 'all';
use File::Copy;
sub process_annotation (@);

my $homepage = "cube.local";

##############################################################################
sub process_input_params(@){


	my ($q,$jobdir,$docx2txt) = @_;
	my $job_type;
	my @input_seq_files = ();
	my $similarity_ckbox = 0;
	#default method for specs is rvet
	my $method = "rvet";


	if ( ! defined $q->param("fnm") || !$q->param("fnm")) {
		html_die ("Please provide sequence file(s) for the analysis.");
	}
	my @upload_filehandles = $q->param("fnm");
	my $size = int @upload_filehandles;

	if( $size == 0){
		html_die ("Please provide sequence file(s) for the analysis.");
	} elsif  ($size > 1) {
		#specs
		$job_type = SPECIALIZATION_WITH_SEQS_PROVIDED;

	} elsif  ($size) {
		#cube with sequence as input
		$job_type = CONSERVATION;
	}

	my ($upload_fhd,  $in_fasta, $in_group, $structure_name);
	my @geneList = ();
	#my $mthd = 0;
	my $ref_seq_name    = "";
	my $gene_nm_file    = 0;
	my $seq_not_aligned = 1;
	my $structure_f     = 0;


	$ref_seq_name = $q->param("qry_nm");
	$ref_seq_name =~ s/\s//g;

	if (defined($q->param("ckb")) && $q->param("ckb")) {
		$seq_not_aligned = 0;
	}


	###########################################################
	# upload sequence files
	for my $upload_fhd ( @upload_filehandles) {

		my @tmp = split(/\\/, $upload_fhd);
		my $filename = pop @tmp;
		my $input_file = "$jobdir/$filename";

		if ( $filename =~ /\.doc$/) {
			my $msg = "&nbsp;\n".
				"By the file name extension (.doc) I am guessing $filename is in a Word document format,\n".
				"which Cube is currently not equipped to handle. Please save your file as .docx, \n".
				"or 'Export' it in Plain Text format, and then upload again in one of these two formats.\n\n".
				"MS Office help pages ".
				"(<a href='http://office.microsoft.com/en-sg/mac-word-help/".
				"save-a-file-in-a-different-file-format-HA102927395.aspx?CTT=5&origin=HA102929513'>click here</a>) ".
				"provide a description on how to save files from Word in different formats.\n\n".
				"Mac users: <a href='http://support.apple.com/kb/PH10512'>read here</a> ".
				"about exporting Plain Text files from Pages'09.\n".
				"(Exporting as docx does not not seem to be supported there.)";
			html_die ($msg);

		} elsif ($filename =~ /\.docx$/) {

			my $docx_file  = $input_file;
			$input_file = $filename;
			$input_file =~ s/\.docx$/\.txt/;
			open(OF, ">$docx_file") || return "Cno: $docx_file:$!\n";
			undef $/;
			print OF <$upload_fhd>;
			$/ = "\n";
			close(OF);

			my $cmd = `$docx2txt  $docx_file $input_file $jobdir`;
			$input_file = "$jobdir/$input_file";
			system($cmd); # looks like this crap gives something on the exit;
			if  (! -e  $input_file || -z $input_file  ) {
				my $msg = "&nbsp;\n".
					"$cmd\n".
					"*********************\n".
					"$input_file\n".
					"*********************\n".
					"Error converting docx to Plain Text format. Exit status: $!.\n".
					"Try saving  your file  in Plain Text format, and then upload again.\n\n".
					"MS Office help pages ".
					"(<a href='http://office.microsoft.com/en-sg/mac-word-help/".
					"save-a-file-in-a-different-file-format-HA102927395.aspx?CTT=5&origin=HA102929513'>click here</a>) ".
					"provide a description on how to save files from Word in different formats.\n\n".
					"Mac users: <a href='http://support.apple.com/kb/PH10512'>read here</a> ".
					"about exporting Plain Text files from Pages'09.\n";
				html_die ($msg);
			}

		} else {
			open(OF, ">$input_file") || return "Cno: $input_file:$!\n";
			undef $/;
			# get rid of carriage return (newline in Windows and Mac)
			my $tmp_container =  <$upload_fhd>;
			$tmp_container    =~ s/\r/\n/g;
			print OF $tmp_container;
			$/ = "\n";
			close(OF);
		}

		push @input_seq_files, $input_file;
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
		# get rid of carriage return (newline in Windows and Mac)
		my $tmp_container =  <$upload_fhd>;
		$tmp_container =~ s/\r/\n/g;
		print OF $tmp_container;
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
		$structure_name, $chainID, $pdb_extract_n_clean, $pdb2seq,
		$fasta_rename, $msf2afa, $mafft,  $muscle, $reorder, $afa2msf, $restrict) = @_;
	my $errmsg = "";

	my @input_seq_files = @{$input_seq_files_ref};
	my @alignment_files = ();
	my $alignment_file;
	my $cmd;
	my $group_name    = "";
	my %group_members = ();
	my $name_resolution_file = "";

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

	my $ref_seq_automatic = 0;
	my $file_ct           = 0;
	my @group_names       = ();

	# check  the alignment file format; transform sf to afa
	for my $input_seq_file (@input_seq_files ) {

		# do we recognize the format?
		$cmd = "grep \" Name:\" $input_seq_file | head -n1";
		my $first_name_line = `$cmd`;
		my $alignment_format = "";

		if($first_name_line){ # we are assuming the msf format

			$alignment_format = "MSF";
			# let's take that MSF represents aligned sequences - this
			# way we don't have to pass the tickmark from ExoLocator
			$seq_not_aligned = 0;
			# otherwise,  we just get rid of the pesky msf input
			my $orig_input_seq_file = $input_seq_file;
			if ( $input_seq_file =~ /\.msf$/ ) {
				$input_seq_file =~ s/msf$/afa/;
			} else {
				$input_seq_file .= ".afa"
			}
			system("$msf2afa  $orig_input_seq_file > $input_seq_file ");
			$alignment_format = "AFA";

		} else {
			$cmd = "grep \">\"  $input_seq_file | head -n1";
			$first_name_line = `$cmd`;
			if($first_name_line){
				$alignment_format = "AFA";
			} else {
				$errmsg = "<P>The alignment format not recognized for $input_seq_file.\n".
					"Check ".
					" <a href=\"http://$homepage/help/gcg_example.txt\">here (GCG, a.k.a. MSF)</a>".
					" and  <a href=\"http://$homepage/help/fasta_example.txt\">here (FASTA)</a>\n" .
					"for  examples of the two formats that the current implementation recognizes.";
				return ($errmsg, "");
			}
		}

		# clean up and simplify names - I think clustalw and such would have already
		# chooped the names, so we have to worry only about afa files
		# 1) grep '>' there is fasta_rename.pl in scripts dir -- see specs.cgi header
		# 2) modify it ouput the original header and the replacement name, and save that info to jobdir
		# 3) make sure that the refseq name correponds to the new shortened name
		$name_resolution_file = "$jobdir/nameindex";
		my $input_seq_backup  = "$input_seq_file.bak"; # what's the purpose of this - more garbage production?
		move($input_seq_file, $input_seq_backup);
		my $suffix;

		if (@input_seq_files==1) {
			$suffix = "";
		} else {
			$file_ct++;
			$suffix = "_g$file_ct"; # gx, as  in "group number x"
		}
		system("$fasta_rename $input_seq_backup $name_resolution_file $suffix  > $input_seq_file");
		`rm $input_seq_backup`;


		# if we still don't have the $ref_seq_name take the first one that appears in the alignment
		if (!$ref_seq_name) {
			#
			if($alignment_format eq "MSF" ){
				$first_name_line = `grep 'Name' $input_seq_file | head -n1`;
				$first_name_line =~ /Name\:\s*(\w+)/;
				(defined $1 && $1) && ($ref_seq_name = $1);

			} else {
				# Reload first name line
				$first_name_line = `grep '>' $input_seq_file | head -n1`;
				$first_name_line =~ />\s*(\w+)/;
				(defined $1 && $1) && ($ref_seq_name = $1);
			}

			$ref_seq_name || html_die ("Unspecified error in the input alignment format.".
				"\n$jobdir\nformat: $alignment_format\nname line: ".
				"$first_name_line\ninput file: $input_seq_file\n");

			$ref_seq_automatic = 1;

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
				push @group_names, $group_name;
			}
		} else {
			$alignment_file  = "$input_seq_file.afa";
		}



		# if not aligned, align
		if ($seq_not_aligned) {
			open (LOG, ">$jobdir/log");
			print LOG "input file  $input_seq_file ($alignment_format  format) not aligned\n";
			close LOG;

			my $errlog;
			#if($alignment_format eq "MSF" ){ #how could this happen ?
			#	$cmd = "$msf2afa $input_seq_file > $input_seq_file.afa";
			#	system($cmd) && html_die ("Error running $cmd\n");
			#	`mv $input_seq_file.afa $input_seq_file`;
			#}

			# muscle reorders, but mafft makes somewhat crappier alignments
			#  mafft is more robust for bigger alignments
			my $number_seqs  = `grep  \'>\' $input_seq_file | wc -l`;
			chomp $number_seqs;
			if ( $number_seqs < 150 ) {
				$cmd = "$muscle -in $input_seq_file -out  $jobdir/tmp.afa >  $jobdir/muscle.out 2>&1";
				system($cmd);
				(-e "$jobdir/tmp.afa" && ! -z "$jobdir/tmp.afa") || html_die("Error running<br>$cmd<br>$!\n");

				if  ( reorder_fasta ($name_resolution_file,  "$jobdir/tmp.afa",  $alignment_file) ) {
					$cmd = "mv  $jobdir/tmp.afa $alignment_file";
					system($cmd) && html_die("Error reordering $name_resolution_file $jobdir/tmp.afa");
				} else {
					`rm  $jobdir/tmp.afa`;
				}

			} else {
				$cmd = "$mafft $input_seq_file 1>  $alignment_file 2>  $jobdir/mafft.out ";
				$errlog = `cat $jobdir/mafft.out`;
				system($cmd) && html_die("Error running $cmd:\n$errlog\n");
			}

		} else {
			# afa, turn to msf
			if($alignment_format eq "AFA" ){
				`cp $input_seq_file  $alignment_file`;
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

	# check the reference sequence name
	if (!$ref_seq_automatic) { # we are trying to figure out what the user has in mind

		my @lines = split "\n", `grep  $ref_seq_name  $name_resolution_file`;
		my ($server_name, $old_name, $orig_hdr);

		if ( @lines == 1) {
			($server_name, $old_name, $orig_hdr) = split "\t", $lines[0];

		} elsif ( @lines < 1) {

			my $errmsg = "Error processing reference sequence name:";
			$errmsg .=   " $ref_seq_name not found in the input.\n$jobdir\n";
			html_die ($errmsg);


		} elsif ( @lines > 1) {

			my $name_found = 0;

			foreach  (@lines) {
				($server_name, $old_name, $orig_hdr) = split "\t";
				if  ($old_name eq $ref_seq_name) {
					$name_found = 1;
					last;
				}
			}
			if ( !$name_found) {
				my $errmsg = "Error processing reference sequence name.";
				$errmsg .=	" More than one name matched the input $ref_seq_name:\n";
				$errmsg .= join "\n", @lines;
				$errmsg .= "\n";
				html_die ($errmsg);
			}
		}

		$ref_seq_name = $server_name;

	}

	# we want one single file
	if (@alignment_files==1) {
		$alignment_file = $alignment_files[0];

	} else {
		# do profile alignment
		my $prev_aln = "$jobdir/prev.afa";
		my $last_aln = "$jobdir/all.afa";
		`cp $alignment_files[0] $last_aln`;
		for my $aln ( @alignment_files[1 .. $#alignment_files] ) {
			`mv  $last_aln $prev_aln`;
			$cmd  = "$muscle -profile -in1 $prev_aln -in2 $aln  -out $last_aln >  $jobdir/muscle.out 2>&1";
			# system  commaind will use bash, usually -- we are ounting on it for the output redirect
			system ($cmd);
			if (-z $last_aln)  {
				my $errlog = `cat $jobdir/muscle.out`;
				my $msg = "Error creating profile alignment.\n".
					"Are your sequences aligned? If not, please ".
					"tick the 'My sequences are not aligned' checkbox.\n";
				diesoft("$msg", "$errlog");
			}
		}
		`rm $prev_aln`;
		$alignment_file = $last_aln;
	}

	my $structure_file         = "";
	my $structure_single_chain = "";

	if ($structure_name) {

		$structure_file = "$jobdir/$structure_name.pdb";

		# we always want a single chain
		if (!$chainID) {
			# if $chainID is given, it is going to be the one
			# if not, sneakpeek for the chain
			my $ret  = `awk \$1=="ATOM" $structure_file`;
			$chainID = substr ( $ret,  21, 1) ||  "A";
		}
		$chainID = uc($chainID);
		# we'll always process, because there is no end to pdb shennanigans
		my $cmd = "$pdb_extract_n_clean $structure_file pdb_$structure_name$chainID $chainID";
		my $ret = `$cmd`;
		$ret && html_die ($ret);

		$structure_single_chain = "$structure_name$chainID";
		# add the structure sequence to the alignment
		my $seq_file =  "$jobdir/$structure_name$chainID.seq";
		# muscle
		#$cmd = "$muscle -profile -in1 $alignment_file  -in2 $seq_file -out $jobdir/tmp.afa";
		# actually lets use mafft - muscle profile can miss tha alignment for the sequence
		# which is already present in the big alignment
		$cmd = "$mafft --add $seq_file $alignment_file  > $jobdir/tmp.afa";
		system($cmd) && html_die ("error running $cmd\n");
		(-z "$jobdir/tmp.afa") && html_die ("error running $cmd:\nthe output is empty\n");
		`mv $jobdir/tmp.afa $alignment_file`;

	}

	my $group_file = "";
	my $ref_group  = "";

	if ($job_type!=CONSERVATION) {

		$ref_group = $group_names[0];

		$group_file = "$jobdir/groups";
		open(GFH, ">$group_file") || html_die ("Error writing to a file (?!)");

		if ($ref_seq_automatic) {

			for $group_name (@group_names) {
				print  GFH  "name  $group_name\n";
				print  GFH  $group_members{$group_name};
				print  GFH  "\n";
			}
			close GFH;

		} else {

			# find ref group corresponding to the ref seq
			my $ordered_names = "";
			for $group_name (@group_names) {
				foreach my $mem (split " ", $group_members{$group_name} ) {
					if ($mem eq $ref_seq_name) {
						$ref_group = $group_name;
					}
				}
			}

			$group_name = $ref_group;
			print  GFH  "name  $group_name\n";
			print  GFH   "$ref_seq_name\n";
			$ordered_names .= "$ref_seq_name\n";
			foreach my $mem (split " ", $group_members{$group_name} ) {
				next if ($mem eq $ref_seq_name);
				print  GFH   "$mem\n";
				$ordered_names .= "$mem\n";
			}
			print  GFH  "\n";


			for $group_name (@group_names) {
				next if $group_name eq  $ref_group;
				print  GFH  "name  $group_name\n";
				print  GFH  $group_members{$group_name};
				print  GFH  "\n";
				$ordered_names .= $group_members{$group_name};
			}
			close GFH;

			($structure_name)  && ($ordered_names .= "pdb_$structure_name$chainID");
			# reorder the alignment  one more time so that the ref group is first,
			# with the reference  sequence on top - easier than hacking itno hypercube
			open ( OF, ">$jobdir/tmp.list") || die "oink?";
			print OF $ordered_names."\n";
			close OF;

			`mv $alignment_file $jobdir/tmp.afa`;
			if  ( reorder_fasta ("$jobdir/tmp.list",  "$jobdir/tmp.afa",  $alignment_file, 8) ) {
				$cmd = "mv  $jobdir/tmp.afa  $alignment_file";
				system($cmd) && html_die("Error reordering $name_resolution_file $jobdir/tmp.afa");
			} else {
				#`rm  $jobdir/tmp.afa  $jobdir/tmp.list`;
			}
		}

	}


	#############################################
	# afa2msf
	my $alignment_file_msf = $alignment_file;
	$alignment_file_msf    =~ s/afa$/msf/;
	$cmd = "$afa2msf  $alignment_file > $alignment_file_msf";
	system($cmd) && html_die ("error running $cmd\n");

	#############################################
	# restrict the sequence to the query
	#

	my $input_name_root = delete_extension($alignment_file);
	my $restricted_msf = "$input_name_root\.restr.msf";
	if($structure_file){
		$cmd = "$restrict $alignment_file_msf '$ref_seq_name' 'pdb_$structure_single_chain' > $restricted_msf";
	} else {
		$cmd = "$restrict $alignment_file_msf $ref_seq_name > $restricted_msf";
	}
	(system $cmd) &&  html_die ("Error running\n$cmd.\n");


	return ("", $ref_seq_name, $ref_group, $restricted_msf, $name_resolution_file,
		$group_file, $structure_name, $structure_file, $structure_single_chain);

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
			if  (defined($tp) && $tp) {
				$tp =~ s/\s//g;
				$tp && push(@annotated_sequence, $tp);
			}
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

=pod
    open (LOG, ">$jobdir/debuglog");

	print LOG "structure_file: $structure_file\n";
	print LOG "$cmd\n";
	print LOG "$alignment_file\n";
=cut
