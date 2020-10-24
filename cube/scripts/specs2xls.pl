#! /usr/bin/perl -w
 
# to install perl Spreadsheet module
# perl -MCPAN -e "install 'Spreadsheet::WriteExcel'"
# doc: 
# http://search.cpan.org/dist/Spreadsheet-WriteExcel/lib/Spreadsheet/WriteExcel.pm

use strict;
use warnings;
use Spreadsheet::WriteExcel;

(@ARGV >= 2) ||
    die "Usage:  cbcvg.pl   <specs score file>  <output name>  \n"; 


my($ranks_file, $outname) = @ARGV;

my @method_names = ('rvet', 'entr', 'ivet', 'majf', 'valdar', 'rvn', 'pheno', 'carb',
		 'entr_s', 'rvs', 'majf_s', 'ivet_s', 'phen_h', 'phen_n');

my $server_version = 1;

my $workbook = Spreadsheet::WriteExcel->new("$outname.xls");
my $worksheet   = $workbook->add_worksheet();
$worksheet->keep_leading_zeros();

##################################################
#set the pallette:
my $COLOR_RANGE = 20;

my $N = 5;
my $C1 = $COLOR_RANGE-1;

my $red = 1.00;
my $green =  0.83;
my $blue =    0.17;
my @color = ();
my @color_name = ();
my @xl_color = ();

$color[0] = "[$red, $green, $blue]";
$color_name[0] = "c0";
$xl_color[0] = $workbook->set_custom_color(8, $red*255, $green*255, $blue*255 );

my $bin_size = $C1/$N;
for (my  $ctr=1; $ctr <= int ($COLOR_RANGE/$N); $ctr++ ) {

    my $ratio =  ( int ( 100*($bin_size- $ctr+1)/$bin_size) ) /100;
    $red   = $ratio;
    $green = $blue = 0;
		 
    $color[$ctr] = "[$red, $green, $blue]"; 
    $color_name[$ctr] = "c$ctr";

    $xl_color[$ctr] = $workbook->set_custom_color($ctr+8, $red*255, $green*255, $blue*255 );	
    #printf "  %d   %d    %d , $ctr, $xl_color[$ctr] \n",$red*255, $green*255, $blue*255;
}

for (my $ctr= int ($COLOR_RANGE/$N)+1 ; $ctr <= $COLOR_RANGE; $ctr++ ) {

    my $ratio =  ( $ctr -  $COLOR_RANGE/$N)/ ($COLOR_RANGE*($N-1)/$N);
    $red = $ratio;
    $green = $blue = $red;

    $xl_color[$ctr] = $workbook->set_custom_color($ctr+8, $red*255, $green*255, $blue*255 );	
    #printf "  %d   %d    %d , $ctr, $xl_color[$ctr] \n",$red*255, $green*255, $blue*255;

  
    $color[$ctr] = "[$red, $green, $blue]"; 
    $color_name[$ctr] = "c$ctr";
}



##################################################
# input/ouput

open (RANKS_FILE, "<$ranks_file") || 
    die "cno $ranks_file\n";
    

my $format_centered = $workbook->add_format();
$format_centered->set_align('center');
my $format_right = $workbook->add_format();
$format_right->set_align('right');
my $format_float = $workbook->add_format();
$format_float->set_num_format('0.00');
#
my$format_left = $workbook->add_format();
$format_left->set_align('left');
#
my $format_hdr = $workbook->add_format(); # Add a format
$format_hdr->set_bold();
$format_hdr->set_border();
$format_hdr->set_align('center');

my $line = 1;
my $last_column = 0;
my @header = ();

while ( <RANKS_FILE> ) {
    next if ( !/\S/ );
    if ( /\%/ ){ # find the column that the specified method is in
		my @aux = split;
		shift @aux;
		@header = @aux;

		if ( $server_version) {
			my @aux2 = ();
			for my  $hdr_field (@aux) {
				if ($hdr_field eq 'surf') {
					push @aux2, "surface";
				} elsif ( grep ($_ =~ $hdr_field, @method_names ) ) {
					push @aux2, " conservation score ($hdr_field) ";
				} else {
					push @aux2, $hdr_field;
				}
			}
			@header = @aux2;
		}
		# header
		$last_column = @header;
		my $column =  chr (ord('A') + $last_column-1);
		$worksheet->set_column("$column:$column", 20);
		$worksheet->write_row(0, 0, \@header, $format_hdr);

	} else {

		chomp;
		my $format;
		my @aux = split;
		$worksheet->write("A$line", '',  $format);

		foreach my $i (0 .. $#aux) {
			my $column =  chr (ord('A') + $i);
			if ( grep ($header[$i] =~ $_, @method_names ) ) {

				my $cvg =  $aux[$i];
				my $color_index = int ($cvg*$COLOR_RANGE );
				# the first column is the color strip
				$format = $workbook->add_format(
					bg_color => $xl_color[$color_index],
					pattern  => 1,
					border   => 1
				);
				$format ->set_num_format('0.00');
				$worksheet->write("$column$line", $aux[$i], $format);

			} elsif ($header[$i] eq 'gaps') {
				$worksheet->write("$column$line", $aux[$i], $format_float);

			} elsif ($header[$i] eq 'annotation') {
				if ($aux[$i] eq  "none")  {
					$aux[$i] = "  ";
				} else {
					$aux[$i]  =~ s/_/ /g;
				}
				$worksheet->write("$column$line", $aux[$i], $format_left);


			} elsif ($header[$i] eq 'surface') {
				if ( $aux[$i] == 1) {
					$worksheet->write("$column$line", "surface", $format_centered);
				}

			} else {

				# generic behavior
				if ( $aux[$i] =~ /\d/ ) {
					$worksheet->write("$column$line", $aux[$i], $format_right);
				} else {
					$worksheet->write("$column$line", $aux[$i], $format_centered);
				}

			}
		}

    }
    $line++;
}


close RANKS_FILE;



##################################################
##################################################
##################################################
##################################################
# colorbar

my $column =  $last_column + 2;
my $row = 2;
$worksheet->write($row, $column, "conserved", $format_right);   
$row = 2+$COLOR_RANGE;
$worksheet->write($row, $column, "variable", $format_right);   



$column =  $last_column + 3;
$row = 0;

$worksheet->write($row, $column, "conservation colorbar", $format_hdr);   

for (my $ctr = 0; $ctr <= $COLOR_RANGE; $ctr++) {
    my $format = $workbook->add_format(
		bg_color => $xl_color[$ctr],
		pattern  => 1,
		border   => 1
	);
    $row = $ctr+2;
    $worksheet->write($row, $column, '',  $format);
}
