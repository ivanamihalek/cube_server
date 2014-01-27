
use strict;

##################################################################################
sub  html_die (@) {
    my $msg  = $_[0];
    my $html = "";

    $html .= html_generic_head();
    $html .= "<div class='main'>\n";   
    $html .= "<table width='75%'  border='0' align='center' cellpadding='0' cellspacing='0' style='overflow:auto'> \n";
    $html .= "<tr ><td align='left'> <left_title>A problem seems to have occured:</left_title> </td><tr> \n";
    $html .= "<tr ><td align='left' style='overflow:auto'> \n";
    $html .= "<pre>$msg</pre> \n";
    #$html .= " $msg\n";
    $html .= "</td></tr>\n";
    $html .= "</table>  \n";  
    $html .= html_generic_body_bottom ();
    print $html;

    exit(1);
}
##################################################################################
##################################################################################
sub html_generic_head(@){

    my $java_script = $_[0];
    my $html="";

    $html .= "Content-type: text/html\n\n";
    $html .= "<html>\n";
    $html .= "<head>\n";
    if($java_script){
	$html .= "<script type='text/javascript' src='$java_script'></script>\n";
    }
    $html .= "<link rel='stylesheet' href='http://eopsf.org/cube/cube_style.css' type='text/css'>\n";
    $html .= "<link rel='stylesheet' href='http://cdn.jsdelivr.net/qtip2/2.0.1/basic/jquery.qtip.min.css'>\n";
    $html .= "<link rel='stylesheet' href='http://eopsf.org/cube/cube_style.css' type='text/css'>\n";
    $html .= "<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>\n";
    $html .= "<script src='http://cdn.jsdelivr.net/qtip2/2.0.1/basic/jquery.qtip.min.js'></script>\n";
    $html .= "<script src='http://eopsf.org/cube/tooltip.js'> </script>\n";
    $html .= "<title> Cube - results page </title>\n";
    $html .= "</head>\n\n";

    $html .= "<body>\n";

    $html .= "<div class='container'>";

    $html .= "    <div class='mainmenu'>";
    $html .= "        <ul>";
    $html .= "            <li><a href='http://eopsf.org/cube/cube.html' >HOME</a></li>";
    $html .= "            <li><a href='http://eopsf.org/cube/help/help.html' >HELP</a></li>";
    $html .= "            <li><a href='http://eopsf.org/cube/code_dwnld.html'>CODE</a></li>";
    $html .= "            <li><a href='http://eopsf.org/'>ABOUT US</a></li>";
    $html .= "        </ul>";
    $html .= "    </div>";

    $html .= "    <!----------------------->";
    $html .= "    <div class='logo'>";
    $html .= "        <img src='http://eopsf.org/cube/images/cube_banner.png' width='830'>";
    $html .= "    </div>";


    return $html;
}


##################################################################################
sub  html_conservation_body_top (@) {

    my ($jobID, $refseq) = @_;
    my $html="";

    $html .= "<div class='main'> \n";

    $html .= "<left_title> Conservation mapped onto $refseq sequence</left_title>\n";
    $html .= "<p> &nbsp; \n";
    $html .= "<img class='centerimg' width='430' src='http://eopsf.org/images/cons_legend.png'>\n" ;

    $html .= "<p>The residues are ranked according to the conservation score, and binned into 5% bins. \n".
	"The bins are colored according to the legend. Note that if 30% or more positions are conserved, \n".
	"the topmost bins will be empty, and the resulting map will be black-and-white.</p>\n";

    $html .= "<p>The results will stay available for a week at this URL:<br>\n".
	"<a href='http://eopsf.org/cgi-bin/cube/specs.cgi?jobID=$jobID' target='new'>\n".
	"http://eopsf.org/cgi-bin/cube/specs.cgi?jobID=$jobID</a></p>\n";
    
    return $html;

}


##################################################################################
sub  html_specialization_body_top (@) {

    my ($jobID, $refseq) = @_;
    my $html="";

    $html .= "<div class='main'>\n";

    $html .= "<left_title> Specialization  mapped onto $refseq sequence</left_title>\n";
    $html .= "<p> &nbsp; \n";

    $html .= "<img class='centerimg' width='420' src='http://eopsf.org/images/cons_spec_legend.png'>\n";

    $html .= "<p>This page shows two different scores side by side.\n".
	"The first one (white-black-red scale) scores the overall conservation, \n".
	"while the other one (blue-white-orange scale) scores the specialization between the sequence groups. \n".
	"Click <a href='http://eopsf.org/cube/help/help.html#output'>here</a> to read more.</p>\n";
    
    $html .= "<p>In either scheme, the residues are ranked according to the score, and binned into 5% bins. \n".
	"The bins are  colored according to the legend. Note that if 30% or more positions are conserved, \n".
	"the topmost bins will be empty, and the resulting conservation map will be black-and-white. \n".
	"The comparable case for the specialization happens when there is no strong specialization signal \n".
	"in the alignment, and all positions appear pale on the colored scale.</p>\n";

    $html .= "<p>The results will stay available for a week at this URL:<br>".
	"<a href='http://eopsf.org/cgi-bin/cube/specs.cgi?jobID=$jobID' target='new'>".
	"http://eopsf.org/cgi-bin/cube/specs.cgi?jobID=$jobID</a></p>\n";
    
    return $html;

}

##################################################################################
sub html_generic_downloadables(@){

    my $html="";
    my $job_type = pop @_;
    my $map_name = pop @_;
    my @downloadables = @_;
    
    $html .= "<p>Downloadables:</p>\n";
    $html .= "<ul>\n";
   
    foreach my $downloadable(@downloadables){

	$downloadable ||  next; # an empty string was passed here

	if(ref($downloadable) eq "ARRAY"){
	    
	    foreach my $png(@{$downloadable}){
		my @tmp = split(/\./, $png);
		(my $from, my $to) = split(/_/, $tmp[$#tmp-1]);
		

		$html .= "<table width=\"100%\">\n";
		$html .= "<tr> <td>&nbsp;&nbsp;</td></tr> \n";
		$html .= "<tr> <td width =\"10%\"> &nbsp;&nbsp;</td> \n";
		$html .= "<td> \n";
		$html .= $map_name;
		$html .= ": positions $from to $to<br>\n";
		$html .= "<img src='./showImg.cgi?params=$png' style='float:center'>\n";
		$html .= "</td></tr> \n";
		$html .= "</table>\n";
	    }

	} elsif($downloadable =~ /(xls)$|(score)$|(zip)$/){
		
	    my $tag="spec";
	    ($job_type==CONSERVATION) && ($tag="cons");

	    if($downloadable =~ /(xls)$/){
            
		$html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'".
		    " title=\" <a href='http://eopsf.org/cube/help/xls_output.html#$tag'>Read more</a> ".
			"about the xls output\">".
		    "per-residue score in xls (spreadsheet) format</a></li>\n";

	    } elsif ($downloadable =~ /(score)$/){
		#$html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'>".
		#    "per-residue  score in plain text format</a></li>\n";

	    } elsif ($downloadable =~ /(zip)$/ ){
		   
		    
		if($downloadable =~ /(\d+\.zip)$/){
		    
		    $html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'".
			" title=\" <a href='http://eopsf.org/cube/help/workdir_output.html#$tag'>Read more</a>".
			" about the contents <br> of Cube's work directory\">".
			"the whole work directory</a></li>\n";

		} elsif($downloadable =~ /\.afa/){
		    $html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'>".
			    "the alignements(sorted by species)</a></li>\n";

		} elsif($downloadable =~ /\.pse/){
		    $html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'".
			" title=\" <a href='http://eopsf.org/cube/help/pymol_output.html#$tag'>Read more</a> ".
			"about the PyMol session\">".
			"pymol session file</a></li>\n";

		} elsif($downloadable =~ /\_specs.py/){
		    $html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'>".
			"chimera session file for specialization</a></li>\n";

		} elsif($downloadable =~ /\_cons.py/){
		    $html .= "<li><a href='http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$downloadable'>".
			"chimera session file for conservation</a></li>\n";
		}
	    }


	} else {
	    $html .= "$downloadable\n";
	}
    }
    $html .="</ul>\n";
    
    return $html;
}


##################################################################################
sub  html_generic_body_bottom (@){

    my $html="";

    $html .= "</div>\n"; # end "main" class

    $html .= "    <div class='footer'>\n";
    $html .= "           By <a href='http://eopsf.org/'>EPSF</a>, \n";
    $html .= "           a part of <a href='http://www.bii.a-star.edu.sg/research/bmad/bmad.php'> \n";
    $html .= "           Biomolecular Modeling and Design Division</a>, \n";
    $html .= "          <a href='http://www.bii.a-star.edu.sg'>BII</a>, ";
    $html .= "          <a href='http://www.a-star.edu.sg'>A*STAR</a>. Design by Harpy.\n";
    $html .= "    </div>\n";

    $html .= "</div>\n</body>\n</html>\n";

    return $html;

}

#######################################################################################
sub  html_spreadsheet_cube(@){ # this is specific for cube output; won't work for specs

    my ($excel_file, $number_of_ref_seqs, $annot_num) = @_;
    my $html     = "";
    my $parser   = Spreadsheet::ParseExcel->new();
    my $workbook = $parser->parse($excel_file);
    

    if ( !defined $workbook ) {
	html_die ($parser->error() . $excel_file);
        return ($parser->error() . $excel_file);
    }

    $html .= "<p>Per-residue scores:</p>";

    $html .= "<div class='exceldiv'>\n";
    $html .= "<table width='800' border='1' align='left' cellpadding='1' cellspacing='0' class='exceltable'>\n"; 
    
    # I can't believe we are parsing the spreadsheet here ...
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
		    if($value !~ /(CONSERVATION|SPECIFICITY|REPRESENTATIVE SEQUENCES|ANNOTATION)/){
			
			if($value){
			    if( ($value =~ /(alm|gaps|pdb_id|pdb_aa|annot)/) ||  ($row<2 && $value =~ /surf/) ){
			    
				$html .= "<td rowspan = '2' width='80' bgcolor='\#$bgcolor_rgb'>$value</td>\n";

			    }  elsif($value =~ /^insert/){

				my $num_colspan = $col_max-7;
				$html .= "<td colspan = '$num_colspan' width='80' ".
				    "bgcolor='\#$bgcolor_rgb'><font size='0.5'>$value</font></td>\n";

			    }  else{
				$html .= "<td width='80' bgcolor='\#$bgcolor_rgb'><font size='0.5'>$value</font></td>\n";
			    }
			}
		
		    }
		    else{
			($value =~ /(CONSERVATION)/) && ($colspan = $number_of_ref_seqs+1);
			($value =~ /(SPECIFICITY)/)  && ($colspan = 1+$number_of_ref_seqs);  # discr + dets for each group
			($value =~ /(REPRESENTATIVE SEQUENCES)/) && ($colspan = $number_of_ref_seqs*2);
			($value =~ /(ANNOTATION)/)   && ($colspan = $annot_num);
			$html .= "<td colspan = '$colspan' align='center' ".
			    "bgcolor='\#$bgcolor_rgb'><font size='1'>$value</font></td>\n";
		    }
		}
		
		
	    }
	    
	    $html .= "</tr>\n";

	}
	
    }
    $html .= "</table>\n";
    $html .= "</div>\n";
    
    return ("", $html);
}


##################################################################################
##################################################################################
sub jmol_script(@); # defined below
sub jmol_applet(@);

sub html_jmol(@) {
    my ($jobdir, $jmol_folder, $pyscript) = @_;
    my ($line,$loading);
    my %color=();
    my %specificity = ();
    my %conservation = ();
    my $html = "";
    

    open(FH, "<$pyscript") || html_die ("Cno:$pyscript");
    while($line = <FH>){
	chomp($line);
	
	my $new_color_scheme = "";
	if($line =~ /^(load)/){
	    my @tmp = split(/\s+/, $line);
	    chop($tmp[1]);
	    $loading = $tmp[1];
	    
	} elsif($line =~ /^(set_color)/){
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

    # write jmol script
    my $cons_script = jmol_script($jobdir,  \%color, \%conservation, $loading, "conservation");
    my $spec_script = jmol_script($jobdir,  \%color, \%specificity,  $loading, "specificity");


    $html .= "<tr><td>";

    $html .= "<table width = '720' border='1' align='center' cellpadding='1' cellspacing='1'>\n";
    $html .= "<tr>\n";
    $html .= jmol_applet ($jmol_folder, $cons_script, "conservation");
    $html .= jmol_applet ($jmol_folder, $spec_script, "specialization");
    $html .= "</tr>\n";
    $html .= "</table>\n";

    $html .= "</td></tr>\n";

    $html .= "<tr><td>\&nbsp;</td></tr>\n";
    return("",$html);


}

###########################################################################################
sub jmol_script(@){

    my ($jobdir, $clr_ref, $scheme_ref, $structure_file, $con_or_spec) = @_;
    my $jmolscript = "";

    $jmolscript .= "load ";
    $jmolscript .= "http://eopsf.org/cgi-bin/struct_server/download.cgi?ID=$structure_file; ";
    
    for my $resi(keys %{$scheme_ref}){
	$jmolscript .= "select $resi; ";
	$jmolscript .= "color ${$clr_ref}{${$scheme_ref}{$resi}}; ";
    }
    $jmolscript .= "select ALL;";
    $jmolscript .= "set frank off;";
    $jmolscript .= "spacefill off;";
    $jmolscript .= "wireframe off;";
    $jmolscript .= "cartoon;";
    $jmolscript .= "trace 40;";

    my $jmolscr_file = $jobdir."/$con_or_spec.jmol";
    open(FH, ">$jmolscr_file") || html_die("Cno:  $jmolscr_file.");
    print FH $jmolscript;
    close(FH);

    return $jmolscript;
    
}


###########################################################################################
sub jmol_applet(@){
    my ($jmol_folder, $jmolscr, $con_or_spec) = @_;
    my $html_script;

    $html_script .= "<td>\n";
    
    
    $html_script .= "<script>\n";
    $html_script .= "jmolHtml('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');\n";
    $html_script .= "jmolHtml('$con_or_spec');\n";
    $html_script .= "jmolInitialize\('$jmol_folder'\);\n";
    $html_script .= "jmolSetAppletColor\('white'\);\n";
    $html_script .= "jmolApplet\(350,'$jmolscr'\);\n";
    $html_script .= "jmolHtml('\&nbsp;\&nbsp;');\n";
    $html_script .= "jmolRadioGroup(\n";
    $html_script .= "[['select ALL; cartoon ONLY; trace 40;', 'cartoon', 'checked'],\n";
    $html_script .= "['select ALL; backbone ONLY; backbone 0.5;', 'backbone'],\n";
    $html_script .= "['select ALL; rocket ONLY;', 'rocket']\n";
    $html_script .= "]);\n";
    $html_script .= "</script>";
    
    $html_script .= "</form>\n";
    $html_script .= "</td>\n";

    return($html_script);
    
}


return 1;