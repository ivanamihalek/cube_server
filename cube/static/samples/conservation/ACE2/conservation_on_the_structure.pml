# To run this file from command line:
# > pymol conservation_on_the_structure.pml
# To run from pymol itself, open pymol and find conservation_on_the_structure.pml
# in the 'File'->'Run Script ...' dropdown menu.

# If you do not have pymol installed, check 
# https://pymolwiki.org/index.php/Windows_Install
# or the links for other platforms at the bottom of that page. 

load 6m17.pdb, the_whole_thing
zoom complete=1
bg_color white
hide everything
select chainB, the_whole_thing and chain B and polymer 
color white,  chainB 
show cartoon, chainB 
show spheres, chainB 
set_color c0 = [1, 0.83, 0.17]
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
color c12, resid 659 and chain B
color c13, resid 425 and chain B
color c11, resid 574 and chain B
color c3, resid 374 and chain B
color c14, resid 76 and chain B
color c10, resid 470 and chain B
color c15, resid 759 and chain B
color c14, resid 471 and chain B
color c16, resid 298 and chain B
color c16, resid 66 and chain B
color c15, resid 483 and chain B
color c5, resid 267 and chain B
color c9, resid 362 and chain B
color c5, resid 543 and chain B
color c13, resid 43 and chain B
color c12, resid 704 and chain B
color c11, resid 419 and chain B
color c14, resid 562 and chain B
color c5, resid 343 and chain B
color c3, resid 408 and chain B
color c10, resid 527 and chain B
color c12, resid 604 and chain B
color c3, resid 327 and chain B
color c5, resid 222 and chain B
color c19, resid 89 and chain B
color c10, resid 389 and chain B
color c19, resid 664 and chain B
color c14, resid 286 and chain B
color c3, resid 395 and chain B
color c6, resid 155 and chain B
color c13, resid 589 and chain B
color c6, resid 468 and chain B
color c3, resid 595 and chain B
color c3, resid 764 and chain B
color c10, resid 37 and chain B
color c12, resid 502 and chain B
color c4, resid 207 and chain B
color c3, resid 302 and chain B
color c7, resid 57 and chain B
color c16, resid 531 and chain B
color c3, resid 530 and chain B
color c14, resid 60 and chain B
color c16, resid 136 and chain B
color c3, resid 331 and chain B
color c11, resid 330 and chain B
color c12, resid 672 and chain B
color c9, resid 738 and chain B
color c7, resid 449 and chain B
color c14, resid 313 and chain B
color c5, resid 434 and chain B
color c11, resid 70 and chain B
color c6, resid 497 and chain B
color c3, resid 513 and chain B
color c9, resid 638 and chain B
color c3, resid 579 and chain B
color c7, resid 654 and chain B
color c8, resid 379 and chain B
color c5, resid 276 and chain B
color c8, resid 458 and chain B
color c3, resid 165 and chain B
color c8, resid 58 and chain B
color c12, resid 754 and chain B
color c17, resid 38 and chain B
color c15, resid 682 and chain B
color c7, resid 533 and chain B
color c12, resid 618 and chain B
color c10, resid 44 and chain B
color c3, resid 414 and chain B
color c15, resid 709 and chain B
color c9, resid 333 and chain B
color c11, resid 310 and chain B
color c3, resid 311 and chain B
color c12, resid 718 and chain B
color c3, resid 511 and chain B
color c8, resid 510 and chain B
color c4, resid 116 and chain B
color c19, resid 609 and chain B
color c8, resid 128 and chain B
color c6, resid 384 and chain B
color c13, resid 669 and chain B
color c16, resid 75 and chain B
color c3, resid 584 and chain B
color c3, resid 726 and chain B
color c3, resid 473 and chain B
color c12, resid 65 and chain B
color c3, resid 480 and chain B
color c6, resid 481 and chain B
color c13, resid 626 and chain B
color c15, resid 541 and chain B
color c12, resid 540 and chain B
color c8, resid 146 and chain B
color c15, resid 257 and chain B
color c5, resid 352 and chain B
color c15, resid 341 and chain B
color c11, resid 340 and chain B
color c13, resid 192 and chain B
color c18, resid 552 and chain B
color c10, resid 748 and chain B
color c3, resid 439 and chain B
color c9, resid 41 and chain B
color c12, resid 105 and chain B
color c3, resid 444 and chain B
color c5, resid 648 and chain B
color c3, resid 406 and chain B
color c6, resid 104 and chain B
color c8, resid 445 and chain B
color c5, resid 487 and chain B
color c13, resid 296 and chain B
color c3, resid 263 and chain B
color c3, resid 385 and chain B
color c18, resid 250 and chain B
color c17, resid 251 and chain B
color c3, resid 399 and chain B
color c5, resid 547 and chain B
color c7, resid 585 and chain B
color c18, resid 159 and chain B
color c3, resid 599 and chain B
color c7, resid 242 and chain B
color c3, resid 347 and chain B
color c3, resid 523 and chain B
color c3, resid 323 and chain B
color c9, resid 172 and chain B
color c5, resid 415 and chain B
color c10, resid 636 and chain B
color c11, resid 138 and chain B
color c3, resid 203 and chain B
color c11, resid 88 and chain B
color c14, resid 736 and chain B
color c19, resid 429 and chain B
color c9, resid 655 and chain B
color c9, resid 164 and chain B
color c17, resid 755 and chain B
color c3, resid 317 and chain B
color c17, resid 212 and chain B
color c8, resid 288 and chain B
color c8, resid 493 and chain B
color c7, resid 466 and chain B
color c3, resid 517 and chain B
color c17, resid 716 and chain B
color c15, resid 118 and chain B
color c10, resid 182 and chain B
color c12, resid 435 and chain B
color c14, resid 87 and chain B
color c17, resid 616 and chain B
color c9, resid 109 and chain B
color c7, resid 201 and chain B
color c4, resid 200 and chain B
color c13, resid 394 and chain B
color c5, resid 665 and chain B
color c8, resid 537 and chain B
color c3, resid 594 and chain B
color c18, resid 337 and chain B
color c10, resid 232 and chain B
color c18, resid 154 and chain B
color c15, resid 765 and chain B
color c13, resid 42 and chain B
color c3, resid 456 and chain B
color c13, resid 491 and chain B
color c3, resid 278 and chain B
color c7, resid 490 and chain B
color c16, resid 692 and chain B
color c13, resid 646 and chain B
color c13, resid 705 and chain B
color c3, resid 477 and chain B
color c6, resid 148 and chain B
color c5, resid 605 and chain B
color c3, resid 746 and chain B
color c7, resid 575 and chain B
color c3, resid 424 and chain B
color c8, resid 253 and chain B
color c4, resid 260 and chain B
color c13, resid 261 and chain B
color c3, resid 375 and chain B
color c3, resid 169 and chain B
color c10, resid 628 and chain B
color c10, resid 520 and chain B
color c4, resid 521 and chain B
color c10, resid 126 and chain B
color c16, resid 59 and chain B
color c14, resid 321 and chain B
color c6, resid 320 and chain B
color c19, resid 728 and chain B
color c13, resid 39 and chain B
color c9, resid 294 and chain B
color c14, resid 532 and chain B
color c16, resid 683 and chain B
color c5, resid 46 and chain B
color c13, resid 670 and chain B
color c18, resid 671 and chain B
color c17, resid 725 and chain B
color c3, resid 237 and chain B
color c3, resid 332 and chain B
color c15, resid 578 and chain B
color c8, resid 625 and chain B
color c3, resid 459 and chain B
color c3, resid 378 and chain B
color c6, resid 719 and chain B
color c10, resid 145 and chain B
color c3, resid 404 and chain B
color c9, resid 73 and chain B
color c13, resid 608 and chain B
color c9, resid 187 and chain B
color c6, resid 619 and chain B
color c14, resid 63 and chain B
color c9, resid 106 and chain B
color c9, resid 501 and chain B
color c5, resid 500 and chain B
color c3, resid 708 and chain B
color c17, resid 301 and chain B
color c11, resid 300 and chain B
color c7, resid 768 and chain B
color c11, resid 353 and chain B
color c4, resid 361 and chain B
color c3, resid 360 and chain B
color c11, resid 193 and chain B
color c3, resid 275 and chain B
color c4, resid 166 and chain B
color c3, resid 561 and chain B
color c10, resid 553 and chain B
color c9, resid 560 and chain B
color c6, resid 129 and chain B
color c17, resid 668 and chain B
color c12, resid 98 and chain B
color c4, resid 464 and chain B
color c17, resid 220 and chain B
color c10, resid 221 and chain B
color c3, resid 29 and chain B
color c12, resid 697 and chain B
color c5, resid 438 and chain B
color c9, resid 649 and chain B
color c18, resid 634 and chain B
color c13, resid 472 and chain B
color c8, resid 749 and chain B
color c15, resid 115 and chain B
color c6, resid 734 and chain B
color c15, resid 40 and chain B
color c9, resid 351 and chain B
color c11, resid 363 and chain B
color c3, resid 350 and chain B
color c9, resid 285 and chain B
color c3, resid 396 and chain B
color c3, resid 542 and chain B
color c18, resid 758 and chain B
color c19, resid 299 and chain B
color c8, resid 563 and chain B
color c3, resid 550 and chain B
color c3, resid 551 and chain B
color c14, resid 596 and chain B
color c17, resid 156 and chain B
color c9, resid 342 and chain B
color c14, resid 247 and chain B
color c12, resid 190 and chain B
color c6, resid 191 and chain B
color c19, resid 658 and chain B
color c7, resid 97 and chain B
color c5, resid 454 and chain B
color c12, resid 223 and chain B
color c17, resid 74 and chain B
color c17, resid 135 and chain B
color c8, resid 409 and chain B
color c12, resid 714 and chain B
color c16, resid 64 and chain B
color c16, resid 614 and chain B
color c3, resid 418 and chain B
color c5, resid 482 and chain B
color c7, resid 681 and chain B
color c7, resid 680 and chain B
color c7, resid 45 and chain B
color c17, resid 426 and chain B
color c15, resid 673 and chain B
color c11, resid 388 and chain B
color c8, resid 124 and chain B
color c4, resid 312 and chain B
color c3, resid 217 and chain B
color c12, resid 469 and chain B
color c3, resid 588 and chain B
color c3, resid 512 and chain B
color c3, resid 177 and chain B
color c9, resid 448 and chain B
color c11, resid 61 and chain B
color c6, resid 639 and chain B
color c13, resid 644 and chain B
color c4, resid 503 and chain B
color c17, resid 303 and chain B
color c16, resid 71 and chain B
color c10, resid 739 and chain B
color c11, resid 744 and chain B
color c3, resid 108 and chain B
color c18, resid 687 and chain B
color c11, resid 645 and chain B
color c18, resid 706 and chain B
color c5, resid 233 and chain B
color c18, resid 210 and chain B
color c17, resid 211 and chain B
color c12, resid 119 and chain B
color c3, resid 606 and chain B
color c16, resid 745 and chain B
color c13, resid 170 and chain B
color c14, resid 171 and chain B
color c18, resid 576 and chain B
color c3, resid 279 and chain B
color c3, resid 183 and chain B
color c5, resid 376 and chain B
color c8, resid 125 and chain B
color c16, resid 99 and chain B
color c3, resid 28 and chain B
color c11, resid 149 and chain B
color c3, resid 715 and chain B
color c3, resid 357 and chain B
color c7, resid 252 and chain B
color c13, resid 134 and chain B
color c16, resid 197 and chain B
color c3, resid 240 and chain B
color c3, resid 241 and chain B
color c7, resid 557 and chain B
color c18, resid 615 and chain B
color c6, resid 436 and chain B
color c18, resid 666 and chain B
color c18, resid 693 and chain B
color c3, resid 284 and chain B
color c14, resid 729 and chain B
color c13, resid 766 and chain B
color c3, resid 455 and chain B
color c3, resid 168 and chain B
color c3, resid 629 and chain B
color c8, resid 367 and chain B
color c5, resid 262 and chain B
color c3, resid 567 and chain B
color c3, resid 635 and chain B
color c5, resid 243 and chain B
color c17, resid 416 and chain B
color c4, resid 522 and chain B
color c15, resid 735 and chain B
color c18, resid 114 and chain B
color c19, resid 322 and chain B
color c7, resid 227 and chain B
color c11, resid 62 and chain B
color c14, resid 690 and chain B
color c17, resid 691 and chain B
color c17, resid 656 and chain B
color c3, resid 274 and chain B
color c3, resid 398 and chain B
color c8, resid 72 and chain B
color c15, resid 756 and chain B
color c13, resid 598 and chain B
color c16, resid 465 and chain B
color c3, resid 158 and chain B
color c15, resid 139 and chain B
color c7, resid 144 and chain B
color c4, resid 405 and chain B
color c18, resid 231 and chain B
color c7, resid 230 and chain B
color c14, resid 677 and chain B
color c3, resid 446 and chain B
color c17, resid 213 and chain B
color c7, resid 492 and chain B
color c11, resid 289 and chain B
color c18, resid 295 and chain B
color c4, resid 173 and chain B
color c10, resid 386 and chain B
color c3, resid 181 and chain B
color c4, resid 180 and chain B
color c3, resid 724 and chain B
color c16, resid 586 and chain B
color c11, resid 507 and chain B
color c18, resid 27 and chain B
color c5, resid 428 and chain B
color c10, resid 307 and chain B
color c4, resid 202 and chain B
color c3, resid 624 and chain B
color c9, resid 685 and chain B
color c16, resid 699 and chain B
color c11, resid 174 and chain B
color c14, resid 647 and chain B
color c7, resid 723 and chain B
color c11, resid 476 and chain B
color c15, resid 258 and chain B
color c3, resid 623 and chain B
color c3, resid 747 and chain B
color c12, resid 143 and chain B
color c3, resid 162 and chain B
color c19, resid 24 and chain B
color c19, resid 214 and chain B
color c3, resid 127 and chain B
color c13, resid 85 and chain B
color c3, resid 355 and chain B
color c7, resid 281 and chain B
color c16, resid 280 and chain B
color c3, resid 717 and chain B
color c18, resid 92 and chain B
color c13, resid 555 and chain B
color c4, resid 189 and chain B
color c15, resid 195 and chain B
color c3, resid 273 and chain B
color c13, resid 102 and chain B
color c12, resid 617 and chain B
color c10, resid 130 and chain B
color c13, resid 131 and chain B
color c18, resid 536 and chain B
color c18, resid 21 and chain B
color c13, resid 239 and chain B
color c3, resid 336 and chain B
color c4, resid 244 and chain B
color c6, resid 457 and chain B
color c17, resid 113 and chain B
color c18, resid 694 and chain B
color c4, resid 179 and chain B
color c13, resid 283 and chain B
color c13, resid 365 and chain B
color c9, resid 80 and chain B
color c5, resid 498 and chain B
color c3, resid 271 and chain B
color c3, resid 270 and chain B
color c5, resid 565 and chain B
color c19, resid 637 and chain B
color c3, resid 225 and chain B
color c11, resid 737 and chain B
color c6, resid 133 and chain B
color c13, resid 422 and chain B
color c6, resid 208 and chain B
color c10, resid 219 and chain B
color c17, resid 23 and chain B
color c16, resid 316 and chain B
color c10, resid 111 and chain B
color c18, resid 110 and chain B
color c14, resid 467 and chain B
color c6, resid 516 and chain B
color c4, resid 407 and chain B
color c7, resid 528 and chain B
color c10, resid 721 and chain B
color c19, resid 720 and chain B
color c17, resid 675 and chain B
color c15, resid 79 and chain B
color c6, resid 184 and chain B
color c3, resid 328 and chain B
color c5, resid 268 and chain B
color c3, resid 621 and chain B
color c7, resid 620 and chain B
color c4, resid 486 and chain B
color c7, resid 69 and chain B
color c3, resid 297 and chain B
color c5, resid 392 and chain B
color c15, resid 140 and chain B
color c4, resid 141 and chain B
color c10, resid 546 and chain B
color c15, resid 592 and chain B
color c14, resid 249 and chain B
color c12, resid 234 and chain B
color c4, resid 152 and chain B
color c6, resid 346 and chain B
color c5, resid 505 and chain B
color c17, resid 86 and chain B
color c20, resid 305 and chain B
color c19, resid 91 and chain B
color c19, resid 662 and chain B
color c3, resid 401 and chain B
color c3, resid 400 and chain B
color c8, resid 235 and chain B
color c11, resid 727 and chain B
color c5, resid 643 and chain B
color c18, resid 762 and chain B
color c9, resid 504 and chain B
color c11, resid 304 and chain B
color c6, resid 743 and chain B
color c6, resid 627 and chain B
color c8, resid 359 and chain B
color c6, resid 22 and chain B
color c7, resid 256 and chain B
color c8, resid 147 and chain B
color c9, resid 290 and chain B
color c4, resid 291 and chain B
color c3, resid 478 and chain B
color c14, resid 185 and chain B
color c17, resid 559 and chain B
color c17, resid 674 and chain B
color c8, resid 199 and chain B
color c15, resid 56 and chain B
color c19, resid 432 and chain B
color c3, resid 123 and chain B
color c6, resid 36 and chain B
color c17, resid 572 and chain B
color c19, resid 30 and chain B
color c14, resid 713 and chain B
color c18, resid 630 and chain B
color c19, resid 631 and chain B
color c7, resid 277 and chain B
color c9, resid 372 and chain B
color c3, resid 50 and chain B
color c11, resid 613 and chain B
color c14, resid 538 and chain B
color c3, resid 730 and chain B
color c4, resid 731 and chain B
color c11, resid 94 and chain B
color c10, resid 338 and chain B
color c8, resid 77 and chain B
color c19, resid 689 and chain B
color c5, resid 364 and chain B
color c11, resid 695 and chain B
color c19, resid 702 and chain B
color c14, resid 564 and chain B
color c15, resid 67 and chain B
color c12, resid 602 and chain B
color c4, resid 453 and chain B
color c3, resid 460 and chain B
color c4, resid 461 and chain B
color c19, resid 224 and chain B
color c16, resid 117 and chain B
color c9, resid 711 and chain B
color c4, resid 710 and chain B
color c18, resid 287 and chain B
color c9, resid 382 and chain B
color c10, resid 318 and chain B
color c3, resid 245 and chain B
color c18, resid 582 and chain B
color c3, resid 518 and chain B
color c3, resid 633 and chain B
color c16, resid 611 and chain B
color c16, resid 610 and chain B
color c6, resid 509 and chain B
color c10, resid 206 and chain B
color c12, resid 733 and chain B
color c16, resid 309 and chain B
color c17, resid 354 and chain B
color c16, resid 137 and chain B
color c11, resid 679 and chain B
color c17, resid 78 and chain B
color c6, resid 194 and chain B
color c3, resid 554 and chain B
color c3, resid 442 and chain B
color c10, resid 496 and chain B
color c6, resid 463 and chain B
color c4, resid 451 and chain B
color c7, resid 450 and chain B
color c14, resid 68 and chain B
color c8, resid 403 and chain B
color c7, resid 652 and chain B
color c14, resid 640 and chain B
color c10, resid 641 and chain B
color c12, resid 215 and chain B
color c15, resid 548 and chain B
color c17, resid 752 and chain B
color c16, resid 93 and chain B
color c15, resid 740 and chain B
color c15, resid 741 and chain B
color c3, resid 348 and chain B
color c4, resid 293 and chain B
color c13, resid 175 and chain B
color c4, resid 266 and chain B
color c17, resid 684 and chain B
color c8, resid 369 and chain B
color c6, resid 412 and chain B
color c3, resid 569 and chain B
color c10, resid 488 and chain B
color c10, resid 120 and chain B
color c13, resid 121 and chain B
color c10, resid 55 and chain B
color c7, resid 526 and chain B
color c12, resid 229 and chain B
color c14, resid 35 and chain B
color c10, resid 326 and chain B
color c3, resid 423 and chain B
color c14, resid 254 and chain B
color c9, resid 132 and chain B
color c17, resid 81 and chain B
color c11, resid 676 and chain B
color c6, resid 447 and chain B
color c8, resid 178 and chain B
color c5, resid 485 and chain B
color c3, resid 499 and chain B
color c8, resid 545 and chain B
color c14, resid 218 and chain B
color c19, resid 387 and chain B
color c14, resid 282 and chain B
color c3, resid 345 and chain B
color c3, resid 587 and chain B
color c7, resid 506 and chain B
color c3, resid 100 and chain B
color c6, resid 101 and chain B
color c14, resid 306 and chain B
color c13, resid 209 and chain B
color c3, resid 366 and chain B
color c3, resid 393 and chain B
color c3, resid 269 and chain B
color c3, resid 566 and chain B
color c18, resid 593 and chain B
color c12, resid 160 and chain B
color c4, resid 161 and chain B
color c15, resid 153 and chain B
color c5, resid 417 and chain B
color c3, resid 529 and chain B
color c14, resid 84 and chain B
color c4, resid 25 and chain B
color c19, resid 329 and chain B
color c4, resid 226 and chain B
color c19, resid 657 and chain B
color c3, resid 315 and chain B
color c12, resid 757 and chain B
color c3, resid 515 and chain B
color c4, resid 248 and chain B
color c4, resid 32 and chain B
color c16, resid 259 and chain B
color c9, resid 391 and chain B
color c12, resid 390 and chain B
color c11, resid 142 and chain B
color c9, resid 356 and chain B
color c8, resid 196 and chain B
color c7, resid 52 and chain B
color c9, resid 151 and chain B
color c19, resid 150 and chain B
color c6, resid 163 and chain B
color c10, resid 590 and chain B
color c3, resid 591 and chain B
color c18, resid 556 and chain B
color c19, resid 698 and chain B
color c3, resid 437 and chain B
color c6, resid 494 and chain B
color c16, resid 26 and chain B
color c19, resid 667 and chain B
color c8, resid 535 and chain B
color c11, resid 335 and chain B
color c8, resid 722 and chain B
color c15, resid 767 and chain B
color c3, resid 204 and chain B
color c11, resid 622 and chain B
color c9, resid 421 and chain B
color c14, resid 420 and chain B
color c3, resid 264 and chain B
color c14, resid 49 and chain B
color c11, resid 686 and chain B
color c11, resid 707 and chain B
color c15, resid 475 and chain B
color c12, resid 83 and chain B
color c3, resid 524 and chain B
color c19, resid 607 and chain B
color c5, resid 112 and chain B
color c8, resid 324 and chain B
color c5, resid 188 and chain B
color c15, resid 577 and chain B
color c3, resid 272 and chain B
color c3, resid 377 and chain B
color c12, resid 103 and chain B
color c12, resid 238 and chain B
color c10, resid 508 and chain B
color c12, resid 427 and chain B
color c4, resid 308 and chain B
color c12, resid 701 and chain B
color c9, resid 700 and chain B
color c8, resid 33 and chain B
color c9, resid 319 and chain B
color c3, resid 443 and chain B
color c18, resid 216 and chain B
color c9, resid 462 and chain B
color c3, resid 519 and chain B
color c10, resid 53 and chain B
color c12, resid 601 and chain B
color c17, resid 600 and chain B
color c14, resid 571 and chain B
color c7, resid 570 and chain B
color c8, resid 176 and chain B
color c3, resid 383 and chain B
color c3, resid 265 and chain B
color c5, resid 371 and chain B
color c3, resid 370 and chain B
color c7, resid 632 and chain B
color c6, resid 583 and chain B
color c3, resid 525 and chain B
color c10, resid 95 and chain B
color c9, resid 474 and chain B
color c16, resid 325 and chain B
color c6, resid 678 and chain B
color c15, resid 732 and chain B
color c16, resid 549 and chain B
color c19, resid 82 and chain B
color c3, resid 292 and chain B
color c3, resid 397 and chain B
color c12, resid 534 and chain B
color c3, resid 349 and chain B
color c18, resid 597 and chain B
color c15, resid 246 and chain B
color c9, resid 157 and chain B
color c14, resid 334 and chain B
color c7, resid 413 and chain B
color c10, resid 430 and chain B
color c3, resid 431 and chain B
color c14, resid 205 and chain B
color c3, resid 402 and chain B
color c19, resid 660 and chain B
color c16, resid 653 and chain B
color c16, resid 661 and chain B
color c6, resid 47 and chain B
color c17, resid 228 and chain B
color c14, resid 368 and chain B
color c12, resid 761 and chain B
color c3, resid 760 and chain B
color c16, resid 753 and chain B
color c3, resid 489 and chain B
color c16, resid 568 and chain B
color c5, resid 495 and chain B
color c3, resid 410 and chain B
color c4, resid 411 and chain B
color c8, resid 167 and chain B
color c14, resid 90 and chain B
color c18, resid 34 and chain B
color c15, resid 122 and chain B
color c8, resid 433 and chain B
color c3, resid 314 and chain B
color c4, resid 54 and chain B
color c5, resid 514 and chain B
color c3, resid 48 and chain B
color c9, resid 651 and chain B
color c6, resid 650 and chain B
color c16, resid 663 and chain B
color c11, resid 696 and chain B
color c8, resid 642 and chain B
color c9, resid 750 and chain B
color c13, resid 763 and chain B
color c11, resid 751 and chain B
color c10, resid 479 and chain B
color c3, resid 358 and chain B
color c4, resid 198 and chain B
color c4, resid 558 and chain B
color c3, resid 742 and chain B
color c3, resid 51 and chain B
color c3, resid 539 and chain B
color c5, resid 544 and chain B
color c13, resid 339 and chain B
color c17, resid 31 and chain B
color c7, resid 703 and chain B
color c3, resid 344 and chain B
color c3, resid 236 and chain B
color c4, resid 441 and chain B
color c9, resid 440 and chain B
color c19, resid 603 and chain B
color c3, resid 452 and chain B
color c6, resid 380 and chain B
color c3, resid 381 and chain B
color c16, resid 255 and chain B
color c7, resid 712 and chain B
color c15, resid 573 and chain B
color c10, resid 581 and chain B
color c13, resid 580 and chain B
color c3, resid 186 and chain B
color c3, resid 373 and chain B
color c13, resid 107 and chain B
color c8, resid 688 and chain B
color c3, resid 96 and chain B
color c6, resid 612 and chain B
color c10, resid 484 and chain B
select heteroatoms,  hetatm and not solvent 
select other_chains, not chain B 
select struct_water, solvent and chain B 
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
zoom  chain B
select poorly_scoring, resid 659+425+574+76+470+759+471+298+66+483+43
select poorly_scoring, poorly_scoring or resid 704+419+562+527+604+89+389+664+286+589+37
select poorly_scoring, poorly_scoring or resid 502+531+60+136+330+672+313+70+754+38+682
select poorly_scoring, poorly_scoring or resid 618+44+709+310+718+609+669+75+65+626+541
select poorly_scoring, poorly_scoring or resid 540+257+341+340+192+552+748+105+296+250+251
select poorly_scoring, poorly_scoring or resid 159+636+138+88+736+429+755+212+716+118+182
select poorly_scoring, poorly_scoring or resid 435+87+616+394+337+232+154+765+42+491+692
select poorly_scoring, poorly_scoring or resid 646+705+261+628+520+59+321+728+39+532+683
select poorly_scoring, poorly_scoring or resid 670+671+725+578+145+608+63+301+300+353+193
select poorly_scoring, poorly_scoring or resid 668+98+220+221+697+634+472+115+40+363+758
select poorly_scoring, poorly_scoring or resid 299+596+156+247+190+658+223+74+135+714+64
select poorly_scoring, poorly_scoring or resid 614+426+673+388+469+61+644+303+71+739+744
select poorly_scoring, poorly_scoring or resid 687+645+706+210+211+119+745+170+171+576+99
select poorly_scoring, poorly_scoring or resid 149+134+197+615+666+693+729+766+416+735+114
select poorly_scoring, poorly_scoring or resid 322+62+690+691+656+756+598+465+139+231+677
select poorly_scoring, poorly_scoring or resid 213+289+295+386+586+507+27+307+699+174+647
select poorly_scoring, poorly_scoring or resid 476+258+143+24+214+85+280+92+555+195+102
select poorly_scoring, poorly_scoring or resid 617+130+131+536+21+239+113+694+283+365+637
select poorly_scoring, poorly_scoring or resid 737+422+219+23+316+111+110+467+721+720+675
select poorly_scoring, poorly_scoring or resid 79+140+592+249+234+86+305+91+662+727+762
select poorly_scoring, poorly_scoring or resid 304+185+559+674+56+432+572+30+713+630+631
select poorly_scoring, poorly_scoring or resid 613+538+94+338+689+695+702+564+67+602+224
select poorly_scoring, poorly_scoring or resid 117+287+318+582+611+610+733+309+354+137+679
select poorly_scoring, poorly_scoring or resid 78+496+68+640+641+215+548+752+93+740+741
select poorly_scoring, poorly_scoring or resid 175+684+488+121+55+229+35+326+254+81+676
select poorly_scoring, poorly_scoring or resid 218+387+282+306+209+593+160+153+84+329+657
select poorly_scoring, poorly_scoring or resid 757+259+390+142+150+556+698+26+667+335+767
select poorly_scoring, poorly_scoring or resid 622+420+49+686+707+475+83+607+577+103+238
select poorly_scoring, poorly_scoring or resid 508+427+701+216+53+601+600+571+95+325+732
select poorly_scoring, poorly_scoring or resid 549+82+534+597+246+334+430+205+660+653+661
select poorly_scoring, poorly_scoring or resid 228+368+761+753+568+90+34+122+663+696+763
select poorly_scoring, poorly_scoring or resid 751+339+31+603+255+573+580+107+484
select poorly_scoring, poorly_scoring and chainB
deselect 
save conservation_on_the_structure.pse 

