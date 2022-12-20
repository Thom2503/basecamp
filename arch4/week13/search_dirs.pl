#!/usr/bin/env perl -w
use strict;
use warnings;

my @files = </home/codegrade/* /home/codegrade/.*>

foreach my $file (@files) {
	opendir(my $dh, $file) || die "Can't open $file: $!";
	while (readdir $dh) {
		print "$file/$_\n";
	}
	closedir $dh;
}