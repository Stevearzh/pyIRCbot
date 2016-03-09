#!/usr/bin/env perl
use strict;
use Getopt::Long;
use Mojo::UserAgent;
use Mojo::Util qw(url_escape encode decode);

my $ua = Mojo::UserAgent->new;

print "群组:\n";
my $group = $ua->get("http://127.0.0.1:3000/openwx/get_group_info")->res->json;
for(@{$group}){
    print encode("utf8",$_->{displayname}) || "NULL","\t",$_->{id},"\n";
}
exit;
