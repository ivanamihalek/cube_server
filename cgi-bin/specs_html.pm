
use strict;

my $homepage = "cube.local";

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
    $html .= "<link rel='stylesheet' href='http://$homepage/cube_style.css' type='text/css'>\n";
    $html .= "<link rel='stylesheet' href='http://cdn.jsdelivr.net/qtip2/2.0.1/basic/jquery.qtip.min.css'>\n";
    $html .= "<link rel='stylesheet' href='http://$homepage/cube_style.css' type='text/css'>\n";
    $html .= "<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>\n";
    $html .= "<script src='http://cdn.jsdelivr.net/qtip2/2.0.1/basic/jquery.qtip.min.js'></script>\n";
    $html .= "<script src='http://$homepage/tooltip.js'> </script>\n";
    $html .= "<title> Cube - results page </title>\n";
    $html .= "</head>\n\n";

    $html .= "<body>\n";

    $html .= "<div class='container'>";

    $html .= "    <div class='mainmenu'>";
    $html .= "        <ul>";
    $html .= "            <li><a href='http://$homepage/cube.html' >HOME</a></li>";
    $html .= "            <li><a href='http://$homepage/help/help.html' >HELP</a></li>";
    $html .= "            <li><a href='http://$homepage/code_dwnld.html'>CODE</a></li>";
    $html .= "            <li><a href='http://$homepage/'>ABOUT US</a></li>";
    $html .= "        </ul>";
    $html .= "    </div>";

    $html .= "    <!----------------------->";
    $html .= "    <div class='logo'>";
    $html .= "        <img src='http://$homepage/images/cube_banner.png' width='830'>";
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
    $html .= "<img class='centerimg' width='430' src='http://$homepage/images/cons_legend.png'>\n" ;

    $html .= "<p>The residues are ranked according to the conservation score, and binned into 5% bins. \n".
	"The bins are colored according to the legend. Note that if 30% or more positions are conserved, \n".
	"the topmost bins will be empty, and the resulting map will be black-and-white. \n".
	"<a href='http://$homepage/help/help.html#exons'  target='new'>Blue bars</a>, when present, indicate exon boundaries.</p>\n";

    $html .= "<p>The results will stay available for a week at this URL:<br>\n".
	"<a href='http://$homepage/cgi-bin/cube/specs.cgi?jobID=$jobID' target='new'>\n".
	"http://$homepage/cgi-bin/cube/specs.cgi?jobID=$jobID</a></p>\n";
    
    return $html;

}


##################################################################################
sub  html_specialization_body_top (@) {

    my ($jobID, $refseq) = @_;
    my $html="";

    $html .= "<div class='main'>\n";

    $html .= "<left_title> Specialization  mapped onto $refseq sequence</left_title>\n";
    $html .= "<p> &nbsp; \n";

    $html .= "<img class='centerimg' width='420' src='http://$homepage/images/cons_spec_legend.png'>\n";

    $html .= "<p>This page shows two different scores side by side.\n".
	"The first one (white-black-red scale) scores the overall conservation, \n".
	"while the other one (blue-white-orange scale) scores the specialization between the sequence groups. \n".
	"Click <a href='http://$homepage/help/help.html#output'>here</a> to read more.</p>\n";
    
    $html .= "<p>In either scheme, the residues are ranked according to the score, and binned into 5% bins. \n".
	"The bins are  colored according to the legend. Note that if 30% or more positions are conserved, \n".
	"the topmost bins will be empty, and the resulting conservation map will be black-and-white. \n".
	"The comparable case for the specialization happens when there is no strong specialization signal \n".
	"in the alignment, and all positions appear pale on the colored scale.</p>\n";

    $html .= "<p>The results will stay available for a week at this URL:<br>".
	"<a href='http://$homepage/cgi-bin/cube/specs.cgi?jobID=$jobID' target='new'>".
	"http://$homepage/cgi-bin/cube/specs.cgi?jobID=$jobID</a></p>\n";
    
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
            
		$html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'".
		    " title=\" <a href='http://$homepage/help/xls_output.html#$tag'>Read more</a> ".
			"about the xls output\">".
		    "per-residue score in xls (spreadsheet) format</a></li>\n";

	    } elsif ($downloadable =~ /(score)$/){
		#$html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'>".
		#    "per-residue  score in plain text format</a></li>\n";

	    } elsif ($downloadable =~ /(zip)$/ ){
		   
		    
		if($downloadable =~ /(\d+\.zip)$/){
		    
		    $html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'".
			" title=\" <a href='http://$homepage/help/workdir_output.html#$tag'>Read more</a>".
			" about the contents <br> of Cube's work directory\">".
			"the whole work directory</a></li>\n";

		} elsif($downloadable =~ /\.afa/){
		    $html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'>".
			    "the alignements(sorted by species)</a></li>\n";

		} elsif($downloadable =~ /\.pse/){
		    $html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'".
			" title=\" <a href='http://$homepage/help/pymol_output.html#$tag'>Read more</a> ".
			"about the PyMol session\">".
			"pymol session file</a></li>\n";

		} elsif($downloadable =~ /\_specs.py/){
		    $html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'>".
			"chimera session file for specialization</a></li>\n";

		} elsif($downloadable =~ /\_cons.py/){
		    $html .= "<li><a href='http://$homepage/cgi-bin/download.cgi?ID=$downloadable'>".
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
	    # $col_max -7 because we are skipping the colorbar legend
            for $col ( $col_min .. ($col_max-7)) {
		$cell = $worksheet->get_cell( $row, $col );
                
		if($cell){
		    $value  = $cell->value();
		    $format = $cell->get_format();
		    # something's off with the naming scheme in xls:
		    # (you would thingk that bg and fg are switched here)
		    my ($pattern, $front_color, $back_color) = @{$format->{Fill}};
		    if ($pattern) {		    
			$bgcolor_rgb = $parser->ColorIdxToRGB($front_color);
		    } else {
			$bgcolor_rgb = "FFFFFF";
		    }
		    
		    if($value !~ /(CONSERVATION|SPECIFICITY|REPRESENTATIVE SEQUENCES|ANNOTATION)/){
			
			if ($value || $value=~/\d/) { # this is the only way I could smuggle the numeric equal to zero through here
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
return 1;
