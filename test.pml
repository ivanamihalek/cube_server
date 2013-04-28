load /tmp/specs_042819024925223/2fyd.pdb, the_whole_thing
create conservation, the_whole_thing and chain A
color white, conservation
hide lines,  conservation
create specificity, conservation
create cns_lalb_orthodb, conservation
create dts_lalb_orthodb, conservation
create cns_lyz_orthodb, conservation
create dts_lyz_orthodb, conservation


hide everything
bg_color white

set_color c0 = [1, 0.87, 0]
set_color c1 = [1, 0, 0]
set_color c2 = [0.73, 0, 0]
set_color c3 = [0.47, 0, 0]
set_color c4 = [0.21, 0, 0]
set_color c5 = [0.0625, 0.0625, 0.0625]
set_color c6 = [0.125, 0.125, 0.125]
set_color c7 = [0.1875, 0.1875, 0.1875]
set_color c8 = [0.25, 0.25, 0.25]
set_color c9 = [0.3125, 0.3125, 0.3125]
set_color c10 = [0.375, 0.375, 0.375]
set_color c11 = [0.4375, 0.4375, 0.4375]
set_color c12 = [0.5, 0.5, 0.5]
set_color c13 = [0.5625, 0.5625, 0.5625]
set_color c14 = [0.625, 0.625, 0.625]
set_color c15 = [0.6875, 0.6875, 0.6875]
set_color c16 = [0.75, 0.75, 0.75]
set_color c17 = [0.8125, 0.8125, 0.8125]
set_color c18 = [0.875, 0.875, 0.875]
set_color c19 = [0.9375, 0.9375, 0.9375]
set_color c20 = [1, 1, 1]

set_color orange0 = [1.0, 1.0, 1.0]
set_color orange1 = [ 1.000,  0.960,  0.920]
set_color orange2 = [ 1.000,  0.920,  0.840]
set_color orange3 = [ 1.000,  0.880,  0.760]
set_color orange4 = [ 1.000,  0.840,  0.680]
set_color orange5 = [ 1.000,  0.800,  0.600]
set_color orange6 = [ 1.000,  0.760,  0.520]
set_color orange7 = [ 1.000,  0.720,  0.440]
set_color orange8 = [ 1.000,  0.680,  0.360]
set_color orange9 = [ 1.000,  0.640,  0.280]
set_color orange10 = [ 1.000,  0.600,  0.200]

set_color berry0  = [1.0, 1.0, 1.0]
set_color berry1  = [ 0.978,  0.908,  0.952]
set_color berry2  = [ 0.956,  0.816,  0.904]
set_color berry3  = [ 0.934,  0.725,  0.856]
set_color berry4  = [ 0.912,  0.633,  0.809]
set_color berry5  = [ 0.890,  0.541,  0.761]
set_color berry6  = [ 0.868,  0.449,  0.713]
set_color berry7  = [ 0.846,  0.358,  0.665]
set_color berry8  = [ 0.824,  0.266,  0.617]
set_color berry9  = [ 0.802,  0.174,  0.569]
set_color berry10  = [ 0.780,  0.082,  0.522]

set_color blue0   = [1.0, 1.0, 1.0]
set_color blue1   = [ 0.900,  0.900,  0.950]
set_color blue2   = [ 0.800,  0.800,  0.900]
set_color blue3   = [ 0.700,  0.700,  0.851]
set_color blue4   = [ 0.600,  0.600,  0.801]
set_color blue5   = [ 0.500,  0.500,  0.751]
set_color blue6   = [ 0.400,  0.400,  0.701]
set_color blue7   = [ 0.300,  0.300,  0.651]
set_color blue8   = [ 0.200,  0.200,  0.602]
set_color blue9   = [ 0.100,  0.100,  0.552]
set_color blue10   = [ 0.000,  0.000,  0.502]

# color by conservation 
color c13, conservation and resid 1 and chain A
color c18, cns_lalb_orthodb and resid 1 and chain A
color c8, cns_lyz_orthodb and resid 1 and chain A
color blue6, specificity and resid 1 and chain A
color blue8, dts_lalb_orthodb and resid 1 and chain A
color orange0, dts_lyz_orthodb and resid 1 and chain A
color c17, conservation and resid 2 and chain A
color c8, cns_lalb_orthodb and resid 2 and chain A
color c16, cns_lyz_orthodb and resid 2 and chain A
color orange5, specificity and resid 2 and chain A
color orange7, dts_lalb_orthodb and resid 2 and chain A
color blue2, dts_lyz_orthodb and resid 2 and chain A
color c18, conservation and resid 3 and chain A
color c14, cns_lalb_orthodb and resid 3 and chain A
color c16, cns_lyz_orthodb and resid 3 and chain A
color orange3, specificity and resid 3 and chain A
color orange0, dts_lalb_orthodb and resid 3 and chain A
color blue3, dts_lyz_orthodb and resid 3 and chain A
color c16, conservation and resid 4 and chain A
color c5, cns_lalb_orthodb and resid 4 and chain A
color c15, cns_lyz_orthodb and resid 4 and chain A
color orange7, specificity and resid 4 and chain A
color orange9, dts_lalb_orthodb and resid 4 and chain A
color blue0, dts_lyz_orthodb and resid 4 and chain A
color c6, conservation and resid 5 and chain A
color c5, cns_lalb_orthodb and resid 5 and chain A
color c7, cns_lyz_orthodb and resid 5 and chain A
color orange7, specificity and resid 5 and chain A
color orange7, dts_lalb_orthodb and resid 5 and chain A
color orange6, dts_lyz_orthodb and resid 5 and chain A
color c1, conservation and resid 6 and chain A
color c4, cns_lalb_orthodb and resid 6 and chain A
color c4, cns_lyz_orthodb and resid 6 and chain A
color blue1, specificity and resid 6 and chain A
color orange1, dts_lalb_orthodb and resid 6 and chain A
color orange1, dts_lyz_orthodb and resid 6 and chain A
color c13, conservation and resid 7 and chain A
color c8, cns_lalb_orthodb and resid 7 and chain A
color c14, cns_lyz_orthodb and resid 7 and chain A
color blue7, specificity and resid 7 and chain A
color blue2, dts_lalb_orthodb and resid 7 and chain A
color blue7, dts_lyz_orthodb and resid 7 and chain A
color c10, conservation and resid 8 and chain A
color c9, cns_lalb_orthodb and resid 8 and chain A
color c7, cns_lyz_orthodb and resid 8 and chain A
color blue3, specificity and resid 8 and chain A
color blue3, dts_lalb_orthodb and resid 8 and chain A
color blue0, dts_lyz_orthodb and resid 8 and chain A
color c7, conservation and resid 9 and chain A
color c15, cns_lalb_orthodb and resid 9 and chain A
color c1, cns_lyz_orthodb and resid 9 and chain A
color orange9, specificity and resid 9 and chain A
color orange1, dts_lalb_orthodb and resid 9 and chain A
color orange9, dts_lyz_orthodb and resid 9 and chain A
color c11, conservation and resid 10 and chain A
color c16, cns_lalb_orthodb and resid 10 and chain A
color c7, cns_lyz_orthodb and resid 10 and chain A
color orange3, specificity and resid 10 and chain A
color blue3, dts_lalb_orthodb and resid 10 and chain A
color orange6, dts_lyz_orthodb and resid 10 and chain A
color c19, conservation and resid 11 and chain A
color c20, cns_lalb_orthodb and resid 11 and chain A
color c16, cns_lyz_orthodb and resid 11 and chain A
color blue5, specificity and resid 11 and chain A
color blue9, dts_lalb_orthodb and resid 11 and chain A
color blue5, dts_lyz_orthodb and resid 11 and chain A
color c7, conservation and resid 12 and chain A
color c6, cns_lalb_orthodb and resid 12 and chain A
color c8, cns_lyz_orthodb and resid 12 and chain A
color blue3, specificity and resid 12 and chain A
color blue1, dts_lalb_orthodb and resid 12 and chain A
color blue1, dts_lyz_orthodb and resid 12 and chain A
color c6, conservation and resid 13 and chain A
color c7, cns_lalb_orthodb and resid 13 and chain A
color c7, cns_lyz_orthodb and resid 13 and chain A
color blue4, specificity and resid 13 and chain A
color blue1, dts_lalb_orthodb and resid 13 and chain A
color blue1, dts_lyz_orthodb and resid 13 and chain A
color c19, conservation and resid 14 and chain A
color c11, cns_lalb_orthodb and resid 14 and chain A
color c20, cns_lyz_orthodb and resid 14 and chain A
color orange2, specificity and resid 14 and chain A
color orange4, dts_lalb_orthodb and resid 14 and chain A
color blue8, dts_lyz_orthodb and resid 14 and chain A
color c14, conservation and resid 15 and chain A
color c16, cns_lalb_orthodb and resid 15 and chain A
color c11, cns_lyz_orthodb and resid 15 and chain A
color orange2, specificity and resid 15 and chain A
color blue4, dts_lalb_orthodb and resid 15 and chain A
color orange0, dts_lyz_orthodb and resid 15 and chain A
color c16, conservation and resid 16 and chain A
color c13, cns_lalb_orthodb and resid 16 and chain A
color c13, cns_lyz_orthodb and resid 16 and chain A
color blue7, specificity and resid 16 and chain A
color blue6, dts_lalb_orthodb and resid 16 and chain A
color blue6, dts_lyz_orthodb and resid 16 and chain A
color c5, conservation and resid 17 and chain A
color c9, cns_lalb_orthodb and resid 17 and chain A
color c8, cns_lyz_orthodb and resid 17 and chain A
color blue5, specificity and resid 17 and chain A
color blue3, dts_lalb_orthodb and resid 17 and chain A
color blue1, dts_lyz_orthodb and resid 17 and chain A
color c9, conservation and resid 18 and chain A
color c6, cns_lalb_orthodb and resid 18 and chain A
color c10, cns_lyz_orthodb and resid 18 and chain A
color blue4, specificity and resid 18 and chain A
color orange0, dts_lalb_orthodb and resid 18 and chain A
color blue3, dts_lyz_orthodb and resid 18 and chain A
color c19, conservation and resid 19 and chain A
color c17, cns_lalb_orthodb and resid 19 and chain A
color c18, cns_lyz_orthodb and resid 19 and chain A
color blue9, specificity and resid 19 and chain A
color blue9, dts_lalb_orthodb and resid 19 and chain A
color blue9, dts_lyz_orthodb and resid 19 and chain A
color c12, conservation and resid 20 and chain A
color c14, cns_lalb_orthodb and resid 20 and chain A
color c6, cns_lyz_orthodb and resid 20 and chain A
color blue5, specificity and resid 20 and chain A
color blue6, dts_lalb_orthodb and resid 20 and chain A
color orange0, dts_lyz_orthodb and resid 20 and chain A
color c15, conservation and resid 21 and chain A
color c11, cns_lalb_orthodb and resid 21 and chain A
color c13, cns_lyz_orthodb and resid 21 and chain A
color blue10, specificity and resid 21 and chain A
color blue9, dts_lalb_orthodb and resid 21 and chain A
color blue10, dts_lyz_orthodb and resid 21 and chain A
color c16, conservation and resid 22 and chain A
color c18, cns_lalb_orthodb and resid 22 and chain A
color c8, cns_lyz_orthodb and resid 22 and chain A
color blue7, specificity and resid 22 and chain A
color blue9, dts_lalb_orthodb and resid 22 and chain A
color orange0, dts_lyz_orthodb and resid 22 and chain A
color c3, conservation and resid 23 and chain A
color c7, cns_lalb_orthodb and resid 23 and chain A
color c4, cns_lyz_orthodb and resid 23 and chain A
color blue1, specificity and resid 23 and chain A
color blue1, dts_lalb_orthodb and resid 23 and chain A
color orange2, dts_lyz_orthodb and resid 23 and chain A
color c12, conservation and resid 24 and chain A
color c16, cns_lalb_orthodb and resid 24 and chain A
color c9, cns_lyz_orthodb and resid 24 and chain A
color orange5, specificity and resid 24 and chain A
color blue1, dts_lalb_orthodb and resid 24 and chain A
color orange6, dts_lyz_orthodb and resid 24 and chain A
color c9, conservation and resid 25 and chain A
color c3, cns_lalb_orthodb and resid 25 and chain A
color c11, cns_lyz_orthodb and resid 25 and chain A
color orange9, specificity and resid 25 and chain A
color orange9, dts_lalb_orthodb and resid 25 and chain A
color orange4, dts_lyz_orthodb and resid 25 and chain A
color c9, conservation and resid 26 and chain A
color c15, cns_lalb_orthodb and resid 26 and chain A
color c3, cns_lyz_orthodb and resid 26 and chain A
color orange3, specificity and resid 26 and chain A
color blue4, dts_lalb_orthodb and resid 26 and chain A
color orange7, dts_lyz_orthodb and resid 26 and chain A
color c14, conservation and resid 27 and chain A
color c15, cns_lalb_orthodb and resid 27 and chain A
color c14, cns_lyz_orthodb and resid 27 and chain A
color orange0, specificity and resid 27 and chain A
color blue2, dts_lalb_orthodb and resid 27 and chain A
color blue2, dts_lyz_orthodb and resid 27 and chain A
color c1, conservation and resid 28 and chain A
color c3, cns_lalb_orthodb and resid 28 and chain A
color c1, cns_lyz_orthodb and resid 28 and chain A
color orange0, specificity and resid 28 and chain A
color orange2, dts_lalb_orthodb and resid 28 and chain A
color orange4, dts_lyz_orthodb and resid 28 and chain A
color c7, conservation and resid 29 and chain A
color c12, cns_lalb_orthodb and resid 29 and chain A
color c5, cns_lyz_orthodb and resid 29 and chain A
color orange8, specificity and resid 29 and chain A
color orange5, dts_lalb_orthodb and resid 29 and chain A
color orange9, dts_lyz_orthodb and resid 29 and chain A
color c17, conservation and resid 30 and chain A
color c18, cns_lalb_orthodb and resid 30 and chain A
color c12, cns_lyz_orthodb and resid 30 and chain A
color orange0, specificity and resid 30 and chain A
color blue6, dts_lalb_orthodb and resid 30 and chain A
color orange0, dts_lyz_orthodb and resid 30 and chain A
color c11, conservation and resid 31 and chain A
color c3, cns_lalb_orthodb and resid 31 and chain A
color c15, cns_lyz_orthodb and resid 31 and chain A
color orange8, specificity and resid 31 and chain A
color orange9, dts_lalb_orthodb and resid 31 and chain A
color blue0, dts_lyz_orthodb and resid 31 and chain A
color c6, conservation and resid 32 and chain A
color c3, cns_lalb_orthodb and resid 32 and chain A
color c11, cns_lyz_orthodb and resid 32 and chain A
color orange6, specificity and resid 32 and chain A
color orange9, dts_lalb_orthodb and resid 32 and chain A
color orange1, dts_lyz_orthodb and resid 32 and chain A
color c9, conservation and resid 33 and chain A
color c17, cns_lalb_orthodb and resid 33 and chain A
color c3, cns_lyz_orthodb and resid 33 and chain A
color orange8, specificity and resid 33 and chain A
color blue0, dts_lalb_orthodb and resid 33 and chain A
color orange9, dts_lyz_orthodb and resid 33 and chain A
color c1, conservation and resid 34 and chain A
color c3, cns_lalb_orthodb and resid 34 and chain A
color c3, cns_lyz_orthodb and resid 34 and chain A
color orange0, specificity and resid 34 and chain A
color orange4, dts_lalb_orthodb and resid 34 and chain A
color orange3, dts_lyz_orthodb and resid 34 and chain A
color c18, conservation and resid 35 and chain A
color c6, cns_lalb_orthodb and resid 35 and chain A
color c18, cns_lyz_orthodb and resid 35 and chain A
color blue7, specificity and resid 35 and chain A
color orange0, dts_lalb_orthodb and resid 35 and chain A
color blue9, dts_lyz_orthodb and resid 35 and chain A
color c10, conservation and resid 36 and chain A
color c15, cns_lalb_orthodb and resid 36 and chain A
color c9, cns_lyz_orthodb and resid 36 and chain A
color blue6, specificity and resid 36 and chain A
color blue7, dts_lalb_orthodb and resid 36 and chain A
color blue1, dts_lyz_orthodb and resid 36 and chain A
color c6, conservation and resid 37 and chain A
color c7, cns_lalb_orthodb and resid 37 and chain A
color c8, cns_lyz_orthodb and resid 37 and chain A
color orange4, specificity and resid 37 and chain A
color orange5, dts_lalb_orthodb and resid 37 and chain A
color orange4, dts_lyz_orthodb and resid 37 and chain A
color c2, conservation and resid 38 and chain A
color c4, cns_lalb_orthodb and resid 38 and chain A
color c3, cns_lyz_orthodb and resid 38 and chain A
color blue1, specificity and resid 38 and chain A
color orange0, dts_lalb_orthodb and resid 38 and chain A
color orange3, dts_lyz_orthodb and resid 38 and chain A
color c19, conservation and resid 39 and chain A
color c13, cns_lalb_orthodb and resid 39 and chain A
color c19, cns_lyz_orthodb and resid 39 and chain A
color blue9, specificity and resid 39 and chain A
color blue8, dts_lalb_orthodb and resid 39 and chain A
color blue9, dts_lyz_orthodb and resid 39 and chain A
color c11, conservation and resid 40 and chain A
color c16, cns_lalb_orthodb and resid 40 and chain A
color c8, cns_lyz_orthodb and resid 40 and chain A
color blue9, specificity and resid 40 and chain A
color blue10, dts_lalb_orthodb and resid 40 and chain A
color blue8, dts_lyz_orthodb and resid 40 and chain A
color c14, conservation and resid 41 and chain A
color c17, cns_lalb_orthodb and resid 41 and chain A
color c10, cns_lyz_orthodb and resid 41 and chain A
color blue6, specificity and resid 41 and chain A
color blue7, dts_lalb_orthodb and resid 41 and chain A
color blue2, dts_lyz_orthodb and resid 41 and chain A
color c8, conservation and resid 42 and chain A
color c10, cns_lalb_orthodb and resid 42 and chain A
color c5, cns_lyz_orthodb and resid 42 and chain A
color orange8, specificity and resid 42 and chain A
color orange6, dts_lalb_orthodb and resid 42 and chain A
color orange8, dts_lyz_orthodb and resid 42 and chain A
color c18, conservation and resid 43 and chain A
color c18, cns_lalb_orthodb and resid 43 and chain A
color c10, cns_lyz_orthodb and resid 43 and chain A
color orange5, specificity and resid 43 and chain A
color blue3, dts_lalb_orthodb and resid 43 and chain A
color orange7, dts_lyz_orthodb and resid 43 and chain A
color c6, conservation and resid 44 and chain A
color c8, cns_lalb_orthodb and resid 44 and chain A
color c5, cns_lyz_orthodb and resid 44 and chain A
color blue3, specificity and resid 44 and chain A
color blue2, dts_lalb_orthodb and resid 44 and chain A
color orange1, dts_lyz_orthodb and resid 44 and chain A
color c18, conservation and resid 45 and chain A
color c12, cns_lalb_orthodb and resid 45 and chain A
color c15, cns_lyz_orthodb and resid 45 and chain A
color orange5, specificity and resid 45 and chain A
color orange5, dts_lalb_orthodb and resid 45 and chain A
color blue2, dts_lyz_orthodb and resid 45 and chain A
color c16, conservation and resid 46 and chain A
color c15, cns_lalb_orthodb and resid 46 and chain A
color c13, cns_lyz_orthodb and resid 46 and chain A
color blue5, specificity and resid 46 and chain A
color blue5, dts_lalb_orthodb and resid 46 and chain A
color blue4, dts_lyz_orthodb and resid 46 and chain A
color c6, conservation and resid 47 and chain A
color c12, cns_lalb_orthodb and resid 47 and chain A
color c1, cns_lyz_orthodb and resid 47 and chain A
color blue2, specificity and resid 47 and chain A
color blue6, dts_lalb_orthodb and resid 47 and chain A
color orange5, dts_lyz_orthodb and resid 47 and chain A
color c6, conservation and resid 48 and chain A
color c12, cns_lalb_orthodb and resid 48 and chain A
color c4, cns_lyz_orthodb and resid 48 and chain A
color blue4, specificity and resid 48 and chain A
color blue5, dts_lalb_orthodb and resid 48 and chain A
color orange2, dts_lyz_orthodb and resid 48 and chain A
color c5, conservation and resid 49 and chain A
color c5, cns_lalb_orthodb and resid 49 and chain A
color c6, cns_lyz_orthodb and resid 49 and chain A
color orange9, specificity and resid 49 and chain A
color orange8, dts_lalb_orthodb and resid 49 and chain A
color orange7, dts_lyz_orthodb and resid 49 and chain A
color c1, conservation and resid 50 and chain A
color c3, cns_lalb_orthodb and resid 50 and chain A
color c1, cns_lyz_orthodb and resid 50 and chain A
color orange1, specificity and resid 50 and chain A
color orange3, dts_lalb_orthodb and resid 50 and chain A
color orange5, dts_lyz_orthodb and resid 50 and chain A
color c1, conservation and resid 51 and chain A
color c3, cns_lalb_orthodb and resid 51 and chain A
color c1, cns_lyz_orthodb and resid 51 and chain A
color orange0, specificity and resid 51 and chain A
color orange2, dts_lalb_orthodb and resid 51 and chain A
color orange4, dts_lyz_orthodb and resid 51 and chain A
color c2, conservation and resid 52 and chain A
color c7, cns_lalb_orthodb and resid 52 and chain A
color c3, cns_lyz_orthodb and resid 52 and chain A
color orange6, specificity and resid 52 and chain A
color orange5, dts_lalb_orthodb and resid 52 and chain A
color orange7, dts_lyz_orthodb and resid 52 and chain A
color c2, conservation and resid 53 and chain A
color c3, cns_lalb_orthodb and resid 53 and chain A
color c3, cns_lyz_orthodb and resid 53 and chain A
color blue0, specificity and resid 53 and chain A
color orange4, dts_lalb_orthodb and resid 53 and chain A
color orange3, dts_lyz_orthodb and resid 53 and chain A
color c1, conservation and resid 54 and chain A
color c3, cns_lalb_orthodb and resid 54 and chain A
color c1, cns_lyz_orthodb and resid 54 and chain A
color orange1, specificity and resid 54 and chain A
color orange4, dts_lalb_orthodb and resid 54 and chain A
color orange5, dts_lyz_orthodb and resid 54 and chain A
color c2, conservation and resid 55 and chain A
color c3, cns_lalb_orthodb and resid 55 and chain A
color c3, cns_lyz_orthodb and resid 55 and chain A
color orange0, specificity and resid 55 and chain A
color orange4, dts_lalb_orthodb and resid 55 and chain A
color orange3, dts_lyz_orthodb and resid 55 and chain A
color c4, conservation and resid 56 and chain A
color c10, cns_lalb_orthodb and resid 56 and chain A
color c3, cns_lyz_orthodb and resid 56 and chain A
color blue3, specificity and resid 56 and chain A
color blue3, dts_lalb_orthodb and resid 56 and chain A
color orange2, dts_lyz_orthodb and resid 56 and chain A
color c4, conservation and resid 57 and chain A
color c7, cns_lalb_orthodb and resid 57 and chain A
color c1, cns_lyz_orthodb and resid 57 and chain A
color orange9, specificity and resid 57 and chain A
color orange8, dts_lalb_orthodb and resid 57 and chain A
color orange9, dts_lyz_orthodb and resid 57 and chain A
color c10, conservation and resid 58 and chain A
color c10, cns_lalb_orthodb and resid 58 and chain A
color c13, cns_lyz_orthodb and resid 58 and chain A
color blue2, specificity and resid 58 and chain A
color blue0, dts_lalb_orthodb and resid 58 and chain A
color blue4, dts_lyz_orthodb and resid 58 and chain A
color c17, conservation and resid 59 and chain A
color c19, cns_lalb_orthodb and resid 59 and chain A
color c10, cns_lyz_orthodb and resid 59 and chain A
color orange2, specificity and resid 59 and chain A
color blue8, dts_lalb_orthodb and resid 59 and chain A
color orange4, dts_lyz_orthodb and resid 59 and chain A
color c1, conservation and resid 60 and chain A
color c4, cns_lalb_orthodb and resid 60 and chain A
color c1, cns_lyz_orthodb and resid 60 and chain A
color blue0, specificity and resid 60 and chain A
color orange1, dts_lalb_orthodb and resid 60 and chain A
color orange5, dts_lyz_orthodb and resid 60 and chain A
color c1, conservation and resid 61 and chain A
color c3, cns_lalb_orthodb and resid 61 and chain A
color c1, cns_lyz_orthodb and resid 61 and chain A
color orange0, specificity and resid 61 and chain A
color orange2, dts_lalb_orthodb and resid 61 and chain A
color orange4, dts_lyz_orthodb and resid 61 and chain A
color c13, conservation and resid 62 and chain A
color c17, cns_lalb_orthodb and resid 62 and chain A
color c9, cns_lyz_orthodb and resid 62 and chain A
color orange6, specificity and resid 62 and chain A
color blue2, dts_lalb_orthodb and resid 62 and chain A
color orange7, dts_lyz_orthodb and resid 62 and chain A
color c7, conservation and resid 63 and chain A
color c14, cns_lalb_orthodb and resid 63 and chain A
color c5, cns_lyz_orthodb and resid 63 and chain A
color blue9, specificity and resid 63 and chain A
color blue9, dts_lalb_orthodb and resid 63 and chain A
color blue7, dts_lyz_orthodb and resid 63 and chain A
color c15, conservation and resid 64 and chain A
color c19, cns_lalb_orthodb and resid 64 and chain A
color c5, cns_lyz_orthodb and resid 64 and chain A
color orange4, specificity and resid 64 and chain A
color blue7, dts_lalb_orthodb and resid 64 and chain A
color orange8, dts_lyz_orthodb and resid 64 and chain A
color c8, conservation and resid 65 and chain A
color c13, cns_lalb_orthodb and resid 65 and chain A
color c4, cns_lyz_orthodb and resid 65 and chain A
color orange7, specificity and resid 65 and chain A
color orange0, dts_lalb_orthodb and resid 65 and chain A
color orange9, dts_lyz_orthodb and resid 65 and chain A
color c10, conservation and resid 66 and chain A
color c19, cns_lalb_orthodb and resid 66 and chain A
color c3, cns_lyz_orthodb and resid 66 and chain A
color orange2, specificity and resid 66 and chain A
color blue8, dts_lalb_orthodb and resid 66 and chain A
color orange8, dts_lyz_orthodb and resid 66 and chain A
color c4, conservation and resid 67 and chain A
color c14, cns_lalb_orthodb and resid 67 and chain A
color c1, cns_lyz_orthodb and resid 67 and chain A
color blue1, specificity and resid 67 and chain A
color blue6, dts_lalb_orthodb and resid 67 and chain A
color orange6, dts_lyz_orthodb and resid 67 and chain A
color c20, conservation and resid 68 and chain A
color c18, cns_lalb_orthodb and resid 68 and chain A
color c19, cns_lyz_orthodb and resid 68 and chain A
color blue6, specificity and resid 68 and chain A
color blue7, dts_lalb_orthodb and resid 68 and chain A
color blue8, dts_lyz_orthodb and resid 68 and chain A
color c8, conservation and resid 69 and chain A
color c5, cns_lalb_orthodb and resid 69 and chain A
color c6, cns_lyz_orthodb and resid 69 and chain A
color orange6, specificity and resid 69 and chain A
color orange7, dts_lalb_orthodb and resid 69 and chain A
color orange6, dts_lyz_orthodb and resid 69 and chain A
color c18, conservation and resid 70 and chain A
color c17, cns_lalb_orthodb and resid 70 and chain A
color c14, cns_lyz_orthodb and resid 70 and chain A
color orange2, specificity and resid 70 and chain A
color blue3, dts_lalb_orthodb and resid 70 and chain A
color blue1, dts_lyz_orthodb and resid 70 and chain A
color c3, conservation and resid 71 and chain A
color c9, cns_lalb_orthodb and resid 71 and chain A
color c5, cns_lyz_orthodb and resid 71 and chain A
color blue3, specificity and resid 71 and chain A
color blue3, dts_lalb_orthodb and resid 71 and chain A
color orange0, dts_lyz_orthodb and resid 71 and chain A
color c12, conservation and resid 72 and chain A
color c6, cns_lalb_orthodb and resid 72 and chain A
color c15, cns_lyz_orthodb and resid 72 and chain A
color orange7, specificity and resid 72 and chain A
color orange8, dts_lalb_orthodb and resid 72 and chain A
color blue1, dts_lyz_orthodb and resid 72 and chain A
color c1, conservation and resid 73 and chain A
color c3, cns_lalb_orthodb and resid 73 and chain A
color c1, cns_lyz_orthodb and resid 73 and chain A
color orange0, specificity and resid 73 and chain A
color orange2, dts_lalb_orthodb and resid 73 and chain A
color orange4, dts_lyz_orthodb and resid 73 and chain A
color c16, conservation and resid 74 and chain A
color c15, cns_lalb_orthodb and resid 74 and chain A
color c14, cns_lyz_orthodb and resid 74 and chain A
color blue9, specificity and resid 74 and chain A
color blue8, dts_lalb_orthodb and resid 74 and chain A
color blue8, dts_lyz_orthodb and resid 74 and chain A
color c11, conservation and resid 75 and chain A
color c4, cns_lalb_orthodb and resid 75 and chain A
color c15, cns_lyz_orthodb and resid 75 and chain A
color blue4, specificity and resid 75 and chain A
color orange2, dts_lalb_orthodb and resid 75 and chain A
color blue7, dts_lyz_orthodb and resid 75 and chain A
color c15, conservation and resid 76 and chain A
color c16, cns_lalb_orthodb and resid 76 and chain A
color c15, cns_lyz_orthodb and resid 76 and chain A
color blue7, specificity and resid 76 and chain A
color blue7, dts_lalb_orthodb and resid 76 and chain A
color blue6, dts_lyz_orthodb and resid 76 and chain A
color c2, conservation and resid 77 and chain A
color c3, cns_lalb_orthodb and resid 77 and chain A
color c3, cns_lyz_orthodb and resid 77 and chain A
color blue0, specificity and resid 77 and chain A
color orange3, dts_lalb_orthodb and resid 77 and chain A
color orange2, dts_lyz_orthodb and resid 77 and chain A
color c18, conservation and resid 78 and chain A
color c17, cns_lalb_orthodb and resid 78 and chain A
color c17, cns_lyz_orthodb and resid 78 and chain A
color blue4, specificity and resid 78 and chain A
color blue5, dts_lalb_orthodb and resid 78 and chain A
color blue7, dts_lyz_orthodb and resid 78 and chain A
color c15, conservation and resid 79 and chain A
color c8, cns_lalb_orthodb and resid 79 and chain A
color c17, cns_lyz_orthodb and resid 79 and chain A
color orange4, specificity and resid 79 and chain A
color orange7, dts_lalb_orthodb and resid 79 and chain A
color blue5, dts_lyz_orthodb and resid 79 and chain A
color c7, conservation and resid 80 and chain A
color c9, cns_lalb_orthodb and resid 80 and chain A
color c3, cns_lyz_orthodb and resid 80 and chain A
color orange0, specificity and resid 80 and chain A
color blue1, dts_lalb_orthodb and resid 80 and chain A
color orange5, dts_lyz_orthodb and resid 80 and chain A
color c5, conservation and resid 81 and chain A
color c3, cns_lalb_orthodb and resid 81 and chain A
color c10, cns_lyz_orthodb and resid 81 and chain A
color blue2, specificity and resid 81 and chain A
color orange1, dts_lalb_orthodb and resid 81 and chain A
color blue3, dts_lyz_orthodb and resid 81 and chain A
color c12, conservation and resid 82 and chain A
color c4, cns_lalb_orthodb and resid 82 and chain A
color c17, cns_lyz_orthodb and resid 82 and chain A
color orange5, specificity and resid 82 and chain A
color orange8, dts_lalb_orthodb and resid 82 and chain A
color blue5, dts_lyz_orthodb and resid 82 and chain A
color c3, conservation and resid 83 and chain A
color c5, cns_lalb_orthodb and resid 83 and chain A
color c9, cns_lyz_orthodb and resid 83 and chain A
color blue3, specificity and resid 83 and chain A
color orange0, dts_lalb_orthodb and resid 83 and chain A
color blue2, dts_lyz_orthodb and resid 83 and chain A
color c9, conservation and resid 84 and chain A
color c8, cns_lalb_orthodb and resid 84 and chain A
color c12, cns_lyz_orthodb and resid 84 and chain A
color blue3, specificity and resid 84 and chain A
color blue1, dts_lalb_orthodb and resid 84 and chain A
color blue4, dts_lyz_orthodb and resid 84 and chain A
color c8, conservation and resid 85 and chain A
color c11, cns_lalb_orthodb and resid 85 and chain A
color c7, cns_lyz_orthodb and resid 85 and chain A
color blue9, specificity and resid 85 and chain A
color blue9, dts_lalb_orthodb and resid 85 and chain A
color blue7, dts_lyz_orthodb and resid 85 and chain A
color c17, conservation and resid 86 and chain A
color c13, cns_lalb_orthodb and resid 86 and chain A
color c17, cns_lyz_orthodb and resid 86 and chain A
color blue8, specificity and resid 86 and chain A
color blue4, dts_lalb_orthodb and resid 86 and chain A
color blue8, dts_lyz_orthodb and resid 86 and chain A
color c10, conservation and resid 87 and chain A
color c3, cns_lalb_orthodb and resid 87 and chain A
color c17, cns_lyz_orthodb and resid 87 and chain A
color orange1, specificity and resid 87 and chain A
color orange8, dts_lalb_orthodb and resid 87 and chain A
color blue8, dts_lyz_orthodb and resid 87 and chain A
color c3, conservation and resid 88 and chain A
color c3, cns_lalb_orthodb and resid 88 and chain A
color c5, cns_lyz_orthodb and resid 88 and chain A
color orange9, specificity and resid 88 and chain A
color orange9, dts_lalb_orthodb and resid 88 and chain A
color orange8, dts_lyz_orthodb and resid 88 and chain A
color c14, conservation and resid 89 and chain A
color c13, cns_lalb_orthodb and resid 89 and chain A
color c10, cns_lyz_orthodb and resid 89 and chain A
color blue8, specificity and resid 89 and chain A
color blue8, dts_lalb_orthodb and resid 89 and chain A
color blue6, dts_lyz_orthodb and resid 89 and chain A
color c19, conservation and resid 90 and chain A
color c18, cns_lalb_orthodb and resid 90 and chain A
color c19, cns_lyz_orthodb and resid 90 and chain A
color blue8, specificity and resid 90 and chain A
color blue8, dts_lalb_orthodb and resid 90 and chain A
color blue9, dts_lyz_orthodb and resid 90 and chain A
color c1, conservation and resid 91 and chain A
color c3, cns_lalb_orthodb and resid 91 and chain A
color c4, cns_lyz_orthodb and resid 91 and chain A
color blue1, specificity and resid 91 and chain A
color orange3, dts_lalb_orthodb and resid 91 and chain A
color orange1, dts_lyz_orthodb and resid 91 and chain A
color c4, conservation and resid 92 and chain A
color c9, cns_lalb_orthodb and resid 92 and chain A
color c4, cns_lyz_orthodb and resid 92 and chain A
color blue1, specificity and resid 92 and chain A
color blue2, dts_lalb_orthodb and resid 92 and chain A
color orange3, dts_lyz_orthodb and resid 92 and chain A
color c4, conservation and resid 93 and chain A
color c6, cns_lalb_orthodb and resid 93 and chain A
color c4, cns_lyz_orthodb and resid 93 and chain A
color blue2, specificity and resid 93 and chain A
color blue0, dts_lalb_orthodb and resid 93 and chain A
color orange2, dts_lyz_orthodb and resid 93 and chain A
color c10, conservation and resid 94 and chain A
color c3, cns_lalb_orthodb and resid 94 and chain A
color c14, cns_lyz_orthodb and resid 94 and chain A
color orange0, specificity and resid 94 and chain A
color orange7, dts_lalb_orthodb and resid 94 and chain A
color blue6, dts_lyz_orthodb and resid 94 and chain A
color c5, conservation and resid 95 and chain A
color c3, cns_lalb_orthodb and resid 95 and chain A
color c11, cns_lyz_orthodb and resid 95 and chain A
color blue7, specificity and resid 95 and chain A
color orange1, dts_lalb_orthodb and resid 95 and chain A
color blue6, dts_lyz_orthodb and resid 95 and chain A
color c5, conservation and resid 96 and chain A
color c8, cns_lalb_orthodb and resid 96 and chain A
color c3, cns_lyz_orthodb and resid 96 and chain A
color orange7, specificity and resid 96 and chain A
color orange6, dts_lalb_orthodb and resid 96 and chain A
color orange8, dts_lyz_orthodb and resid 96 and chain A
color c13, conservation and resid 97 and chain A
color c11, cns_lalb_orthodb and resid 97 and chain A
color c16, cns_lyz_orthodb and resid 97 and chain A
color orange5, specificity and resid 97 and chain A
color orange6, dts_lalb_orthodb and resid 97 and chain A
color blue3, dts_lyz_orthodb and resid 97 and chain A
color c17, conservation and resid 98 and chain A
color c19, cns_lalb_orthodb and resid 98 and chain A
color c12, cns_lyz_orthodb and resid 98 and chain A
color orange3, specificity and resid 98 and chain A
color blue7, dts_lalb_orthodb and resid 98 and chain A
color orange1, dts_lyz_orthodb and resid 98 and chain A
color c17, conservation and resid 99 and chain A
color c14, cns_lalb_orthodb and resid 99 and chain A
color c11, cns_lyz_orthodb and resid 99 and chain A
color orange7, specificity and resid 99 and chain A
color orange2, dts_lalb_orthodb and resid 99 and chain A
color orange5, dts_lyz_orthodb and resid 99 and chain A
color c4, conservation and resid 100 and chain A
color c5, cns_lalb_orthodb and resid 100 and chain A
color c4, cns_lyz_orthodb and resid 100 and chain A
color blue1, specificity and resid 100 and chain A
color orange0, dts_lalb_orthodb and resid 100 and chain A
color orange1, dts_lyz_orthodb and resid 100 and chain A
color c9, conservation and resid 101 and chain A
color c6, cns_lalb_orthodb and resid 101 and chain A
color c10, cns_lyz_orthodb and resid 101 and chain A
color blue5, specificity and resid 101 and chain A
color blue0, dts_lalb_orthodb and resid 101 and chain A
color blue4, dts_lyz_orthodb and resid 101 and chain A
color c18, conservation and resid 102 and chain A
color c12, cns_lalb_orthodb and resid 102 and chain A
color c18, cns_lyz_orthodb and resid 102 and chain A
color orange3, specificity and resid 102 and chain A
color orange4, dts_lalb_orthodb and resid 102 and chain A
color blue5, dts_lyz_orthodb and resid 102 and chain A
color c3, conservation and resid 103 and chain A
color c7, cns_lalb_orthodb and resid 103 and chain A
color c5, cns_lyz_orthodb and resid 103 and chain A
color orange8, specificity and resid 103 and chain A
color orange7, dts_lalb_orthodb and resid 103 and chain A
color orange8, dts_lyz_orthodb and resid 103 and chain A
color c1, conservation and resid 104 and chain A
color c3, cns_lalb_orthodb and resid 104 and chain A
color c4, cns_lyz_orthodb and resid 104 and chain A
color blue0, specificity and resid 104 and chain A
color orange3, dts_lalb_orthodb and resid 104 and chain A
color orange1, dts_lyz_orthodb and resid 104 and chain A
color c8, conservation and resid 105 and chain A
color c14, cns_lalb_orthodb and resid 105 and chain A
color c8, cns_lyz_orthodb and resid 105 and chain A
color orange7, specificity and resid 105 and chain A
color orange1, dts_lalb_orthodb and resid 105 and chain A
color orange7, dts_lyz_orthodb and resid 105 and chain A
color c3, conservation and resid 106 and chain A
color c4, cns_lalb_orthodb and resid 106 and chain A
color c6, cns_lyz_orthodb and resid 106 and chain A
color blue2, specificity and resid 106 and chain A
color orange0, dts_lalb_orthodb and resid 106 and chain A
color orange0, dts_lyz_orthodb and resid 106 and chain A
color c2, conservation and resid 107 and chain A
color c6, cns_lalb_orthodb and resid 107 and chain A
color c1, cns_lyz_orthodb and resid 107 and chain A
color orange9, specificity and resid 107 and chain A
color orange8, dts_lalb_orthodb and resid 107 and chain A
color orange9, dts_lyz_orthodb and resid 107 and chain A
color c12, conservation and resid 108 and chain A
color c9, cns_lalb_orthodb and resid 108 and chain A
color c12, cns_lyz_orthodb and resid 108 and chain A
color blue8, specificity and resid 108 and chain A
color blue4, dts_lalb_orthodb and resid 108 and chain A
color blue6, dts_lyz_orthodb and resid 108 and chain A
color c15, conservation and resid 109 and chain A
color c14, cns_lalb_orthodb and resid 109 and chain A
color c16, cns_lyz_orthodb and resid 109 and chain A
color orange2, specificity and resid 109 and chain A
color blue0, dts_lalb_orthodb and resid 109 and chain A
color blue5, dts_lyz_orthodb and resid 109 and chain A
color c15, conservation and resid 110 and chain A
color c10, cns_lalb_orthodb and resid 110 and chain A
color c15, cns_lyz_orthodb and resid 110 and chain A
color orange6, specificity and resid 110 and chain A
color orange7, dts_lalb_orthodb and resid 110 and chain A
color blue0, dts_lyz_orthodb and resid 110 and chain A
color c1, conservation and resid 111 and chain A
color c3, cns_lalb_orthodb and resid 111 and chain A
color c3, cns_lyz_orthodb and resid 111 and chain A
color blue0, specificity and resid 111 and chain A
color orange3, dts_lalb_orthodb and resid 111 and chain A
color orange2, dts_lyz_orthodb and resid 111 and chain A
color c15, conservation and resid 112 and chain A
color c17, cns_lalb_orthodb and resid 112 and chain A
color c13, cns_lyz_orthodb and resid 112 and chain A
color orange3, specificity and resid 112 and chain A
color blue3, dts_lalb_orthodb and resid 112 and chain A
color blue0, dts_lyz_orthodb and resid 112 and chain A
color c16, conservation and resid 113 and chain A
color c10, cns_lalb_orthodb and resid 113 and chain A
color c17, cns_lyz_orthodb and resid 113 and chain A
color orange5, specificity and resid 113 and chain A
color orange6, dts_lalb_orthodb and resid 113 and chain A
color blue3, dts_lyz_orthodb and resid 113 and chain A
color c9, conservation and resid 114 and chain A
color c13, cns_lalb_orthodb and resid 114 and chain A
color c6, cns_lyz_orthodb and resid 114 and chain A
color orange4, specificity and resid 114 and chain A
color blue2, dts_lalb_orthodb and resid 114 and chain A
color orange6, dts_lyz_orthodb and resid 114 and chain A
color c7, conservation and resid 115 and chain A
color c3, cns_lalb_orthodb and resid 115 and chain A
color c11, cns_lyz_orthodb and resid 115 and chain A
color blue9, specificity and resid 115 and chain A
color blue7, dts_lalb_orthodb and resid 115 and chain A
color blue9, dts_lyz_orthodb and resid 115 and chain A
color c13, conservation and resid 116 and chain A
color c9, cns_lalb_orthodb and resid 116 and chain A
color c17, cns_lyz_orthodb and resid 116 and chain A
color orange4, specificity and resid 116 and chain A
color orange6, dts_lalb_orthodb and resid 116 and chain A
color blue4, dts_lyz_orthodb and resid 116 and chain A
color c14, conservation and resid 117 and chain A
color c3, cns_lalb_orthodb and resid 117 and chain A
color c18, cns_lyz_orthodb and resid 117 and chain A
color blue0, specificity and resid 117 and chain A
color orange8, dts_lalb_orthodb and resid 117 and chain A
color blue8, dts_lyz_orthodb and resid 117 and chain A
color c2, conservation and resid 118 and chain A
color c3, cns_lalb_orthodb and resid 118 and chain A
color c3, cns_lyz_orthodb and resid 118 and chain A
color orange9, specificity and resid 118 and chain A
color orange9, dts_lalb_orthodb and resid 118 and chain A
color orange9, dts_lyz_orthodb and resid 118 and chain A
color c19, conservation and resid 119 and chain A
color c18, cns_lalb_orthodb and resid 119 and chain A
color c16, cns_lyz_orthodb and resid 119 and chain A
color blue8, specificity and resid 119 and chain A
color blue9, dts_lalb_orthodb and resid 119 and chain A
color blue7, dts_lyz_orthodb and resid 119 and chain A
color c1, conservation and resid 120 and chain A
color c3, cns_lalb_orthodb and resid 120 and chain A
color c1, cns_lyz_orthodb and resid 120 and chain A
color orange0, specificity and resid 120 and chain A
color orange2, dts_lalb_orthodb and resid 120 and chain A
color orange4, dts_lyz_orthodb and resid 120 and chain A
color c17, conservation and resid 121 and chain A
color c11, cns_lalb_orthodb and resid 121 and chain A
color c16, cns_lyz_orthodb and resid 121 and chain A
color orange4, specificity and resid 121 and chain A
color orange5, dts_lalb_orthodb and resid 121 and chain A
color blue3, dts_lyz_orthodb and resid 121 and chain A
color c11, conservation and resid 122 and chain A
color c20, cns_lalb_orthodb and resid 122 and chain A
color c10, cns_lyz_orthodb and resid 122 and chain A
color orange4, specificity and resid 122 and chain A
color orange0, dts_lalb_orthodb and resid 122 and chain A
color orange6, dts_lyz_orthodb and resid 122 and chain A
color c20, conservation and resid 123 and chain A
color c20, cns_lalb_orthodb and resid 123 and chain A
color c20, cns_lyz_orthodb and resid 123 and chain A
color orange0, specificity and resid 123 and chain A
color orange0, dts_lalb_orthodb and resid 123 and chain A
color orange0, dts_lyz_orthodb and resid 123 and chain A

deselect
zoom complete=1
show spheres, cns_lalb_orthodb
show spheres, dts_lalb_orthodb
show spheres, cns_lyz_orthodb
show spheres, dts_lyz_orthodb
show spheres, conservation
show spheres, specificity
select heteroatoms,  hetatm and not solvent 
select other_chains, not chain A 
select struct_water, solvent and chain A 
select metals, symbol  mg+ca+fe+zn+na+k+mn+cu+ni+cd+i
cartoon putty 
show  cartoon,  other_chains 
hide  spheres,   heteroatoms 
show  sticks,   heteroatoms 
show  spheres,  struct_water 
show  spheres,  metals 
color palecyan, struct_water 
color lightteal, other_chains or heteroatoms 
color magenta, metals
zoom  chain A
deselect 
