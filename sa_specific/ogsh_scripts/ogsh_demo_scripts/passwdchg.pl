#!/usr/bin/perl
#
# Usage: change_password [<username>]
#
# Changes password by directly updating /etc/shadow on each server
# that you have root Opsware Global Filesystem Access to and that belongs
# to the "UNIX Servers" Public group. This is just an example of how you
# can use the OGFS. Additional things to do in a production grade script:
#
# - update the last password change field
# - use Crypt::PasswdMD5 unix_md5_crypt() instead of built-in crypt() when
#   appropriate
# - use a different salt to crypt the password for each server
# - check if username exists in /etc/shadow before blithly using "-i"
#   in the change_password() function.
#

use strict;

use constant PUBLIC_GROUPS => '/opsw/Server/@Group/Public';
use constant UNIX_SERVERS  => PUBLIC_GROUPS . '/UNIX Servers/@';

sub prompt_password {
	my ($user) = @_;
	my @salt = ('.', '/', 0 .. 9, 'A' .. 'Z', 'a' .. 'z');
	my $salt = join('', map{$salt[rand @salt]} (0..1));
	my $pass;
	print "Changing password for $user.\n";
	print "password for $user:";
	system "stty -echo";
	chomp($pass = <STDIN>);
	print "\n";
	system "stty echo";
	my $des_pass = crypt($pass, $salt);
	return $des_pass;
}

sub change_password {
	my ($path, $user, $pass) = @_;
	# see perlfaq5: How can I use Perl's "-i" option from within a program?
	my $rv = 0;
	local($^I, @ARGV) = ('.old', $path);
	while(<>) {
		next unless /^$user:/;
		my @fields = split(/:/);
		$fields[1] = $pass;
		$_ = join(':', @fields);
		$rv = 1;
	} continue {
		print;
	}
	return $rv;
}

sub listdir {
	my ($path) = @_;
	my ($dir, @files);
	opendir($dir, $path) or die "opendir($path): $!\n";
	@files = readdir($dir);
	closedir($dir);
	return @files;
}

sub main {
	my $user = $ARGV[0] ? $ARGV[0] : (getpwuid($<))[0];
	my $pass = prompt_password($user);
	foreach my $server (listdir(UNIX_SERVERS)) {
		my $etc_shadow = 
			join("/", UNIX_SERVERS, $server, "files/root/etc/shadow");
		next unless -r $etc_shadow;
		print "Password for $user changed on $server.\n" if
			change_password($etc_shadow, $user, $pass);
	}
}

main();
exit 0;

