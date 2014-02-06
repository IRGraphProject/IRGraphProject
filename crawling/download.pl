#! /usr/bin/perl

use MediaWiki::API;

my $mw = MediaWiki::API->new();
$mw->{config}->{api_url} = 'http://en.wikipedia.org/w/api.php';

my @titles;
open(my $titlefile, "<", "titles.txt") or die "Failed to open file";

@titles = <$titlefile>;

while(scalar(@titles) !=0)
{
	$pagename=shift(@titles);
	my $ref = $mw->get_page( { title => $_ } );
	unless ( $ref->{missing} ) {
		print $ref->{'*'};
	}
}
# and print the article titles
#foreach (@{$articles}) {
#	print "$_->{title}\n";
#}

#foreach (@titles) {
#	my $page = $mw->get_page( { title => $_ } );
#	print $page->{'*'};
#
#}
