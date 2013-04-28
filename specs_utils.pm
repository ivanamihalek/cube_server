use strict;

##################################################################################################
sub zip_directory(@){
    my ($zip, $jobdir)  = @_;
    my $dirzipfile      = "$jobdir.zip";
    my @absolute_path   = split "/", $jobdir;
    my $jobdir_name     = pop @absolute_path;
    my $one_level_above = join "/", @absolute_path;
    my $pwd = `pwd`;
    chomp $pwd;
    chdir $one_level_above;
    my $cmd = "$zip -r $dirzipfile $jobdir_name > /dev/null";
    system($cmd) && ($dirzipfile = "");
    chdir $pwd;
    return $dirzipfile;
}

##################################################################################################
sub zip_file(@){
    my ($zip, $fullpath)  = @_;
    
    my @absolute_path   = split "/", $fullpath;
    my $file    = pop @absolute_path;
    my $jobdir  = join "/", @absolute_path;
    my $zipfile = "$file.zip";
    my $pwd = `pwd`;
    chomp $pwd;
    chdir $jobdir;
    my $cmd = "$zip  $zipfile $file > /dev/null";
    system($cmd) && ($zipfile = "");
    chdir $pwd;
    return $jobdir."/".$zipfile;
}


#############################################################################################
sub add_annotation(@){

    my ($score_file, $seq_annotation_ref, $name_resolution_file, $alm_msf) = @_;
    my $score_annot_file = $score_file . ".annotated";
    my $tmp_file = $score_file . ".tmp";

    my %seq_annotation = %{$seq_annotation_ref};
    my @annotated_seqs_user = keys %seq_annotation; 

    ############################################
    # read in the alignment
    open(MSF, "<$alm_msf")||html_die("Cno:$alm_msf");
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

	    if ( defined $sequence{$name} ) {
		$sequence{$name} .= $aux_str;
	    } else {
		push @names, $name;
		$sequence{$name}  = $aux_str;
	    }
	} 
    } while ( <MSF>);

    ############################################
    # name resolution
    my %name_translation = ();
    foreach my $user_name (@annotated_seqs_user ) {
	my @lines = split "\n", `grep  $user_name  $name_resolution_file`;
	if ( @lines > 1) {
	    my $errmsg = "Error processing the annotation.";
	    $errmsg .=	" More than one name matched the input $user_name:\n";
	    $errmsg .= join "\n", @lines;
	    $errmsg .= "\n";
	    html_die ($errmsg);

	} elsif ( @lines < 1) {
	    my $errmsg = "Error processing the annotation.";
	    $errmsg .=	" $user_name not found in the input.\n"; 
	    html_die ($errmsg);

	}
	my ($server_name, $oldname, $orig_hdr) = split "\t", $lines[0];
	$name_translation{$user_name} = $server_name;
    }

    ############################################
    # turn the msf into a table (first index= sequence, 2nd index= position
    my $seq = 0;
    my (%array,%counter,%seqno);

    ############################################
    # recalculate the position numbers for each annotated sequence
    foreach my $user_name (@annotated_seqs_user ) {
	
	my $server_name = $name_translation{$user_name};
	my @aux = split '', $sequence{$server_name};

	foreach my $pos ( 0 .. $#aux ) {
	    $array{$server_name}[$pos] = $aux[$pos];
	    if ( $aux[$pos] !~ /[\.\-]/ ) {
		(defined  $counter{$server_name}) || ($counter{$server_name} = 0);
		# take care of the fact that people count from 1
		# by incrementing first
		$counter{$server_name} ++; 
		$seqno{$server_name}[$pos] = $counter{$server_name};
	    } else {
		$seqno{$server_name}[$pos] = "-";
	    }
	}
	$seq++;
    }

    ##############################################
    #  output
    open(OFH,">$tmp_file")||return("Cno:$tmp_file");
    print OFH " annotation \n"; # header

    # [ZH: ] here random chose $annot_name[0],since all seq are the same length with gappes
    my $alignment_length = length ((values %sequence)[0]);

    for my $pos (0 .. $alignment_length-1) { 
	    
	my $annot_str = "";
	
	foreach my $user_name (@annotated_seqs_user ) {
	    
	    my $server_name = $name_translation{$user_name};
	    my $pos_map     = $seqno{$server_name}[$pos];

	    if (defined $seq_annotation{$user_name}[$pos_map]) {
		$annot_str && ($annot_str.="; ");
		$annot_str .= $seq_annotation{$user_name}[$pos_map];
	    }
	}
	$annot_str || ($annot_str="none");
	$annot_str  =~ s/\s/_/g;
	$annot_str .= "\n";
	print OFH $annot_str;
    }
    close (OFH);

    `pr -m -t -s $score_file $tmp_file > $score_annot_file`;
    `rm $tmp_file`;

 
    return  $score_annot_file;
}


return 1;
