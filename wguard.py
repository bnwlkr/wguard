#!/usr/bin/env python

import argparse
import sys

hosts_file_path = "/etc/hosts"
ipv4_block_address = "127.0.0.1"
ipv6_block_address = "::1"

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def get_domain(hosts_file_line):
	return hosts_file_line.split()[1]

def get_block_address(hosts_file_line):
	return hosts_file_line.split()[0]

def is_blocked_entry(hosts_file_line):
	if len(hosts_file_line.split()) != 2: return False
	is_blocked_ipv4 = get_block_address(hosts_file_line) == ipv4_block_address
	is_blocked_ipv6 = get_block_address(hosts_file_line) == ipv6_block_address
	is_domain_localhost = get_domain(hosts_file_line) == "localhost"
	return (is_blocked_ipv4 or is_blocked_ipv6) and not is_domain_localhost

def list_blocked():
	blocked = set()
	with open(hosts_file_path, 'r') as hosts_file:
		for hosts_file_line in hosts_file.read().splitlines():
			if is_blocked_entry(hosts_file_line):
				domain = get_domain(hosts_file_line)
				if not domain.startswith("www"):
					blocked.add(get_domain(hosts_file_line))
	print(bcolors.BOLD + "Blocked websites: " + bcolors.ENDC)
	for domain_name in blocked:
		print("\t" + domain_name)
	
	
def block(domain_name, quiet=False):
	with open(hosts_file_path, "r") as hosts_file:
		current_hosts_file_contents = hosts_file.read()
	for hosts_file_line in current_hosts_file_contents.splitlines():
		if is_blocked_entry(hosts_file_line) and get_domain(hosts_file_line) == domain_name:
			if not quiet: print(bcolors.OKBLUE + "%s is already blocked" % domain_name + bcolors.ENDC)
			return
	new_entry = "%-15s %s\n%-15s %s\n" % (ipv4_block_address, domain_name, ipv6_block_address, domain_name)
	with open(hosts_file_path, "a") as hosts_file:
		if current_hosts_file_contents[-1] != "\n":
			hosts_file.write("\n")
		hosts_file.write(new_entry)
	if not quiet: print(bcolors.OKGREEN + "Blocked %s" % domain_name + bcolors.ENDC)

def unblock(domain_name, quiet=False):
	logged_unblock = False
	with open(hosts_file_path, 'r') as hosts_file:
		hosts_file_lines = hosts_file.read().splitlines()
	with open(hosts_file_path, 'w') as hosts_file:
		for hosts_file_line in hosts_file_lines:
			if is_blocked_entry(hosts_file_line):
				if get_domain(hosts_file_line) == domain_name:
					if not logged_unblock:
						if not quiet: print(bcolors.OKGREEN + "Unblocked %s" % domain_name + bcolors.ENDC)
						logged_unblock = True
					continue
			hosts_file.write(hosts_file_line + "\n")
	if not logged_unblock:
		if not quiet: print(bcolors.OKBLUE + "wguard wasn't blocking %s" % domain_name + bcolors.ENDC)
	
def main():
	parser = argparse.ArgumentParser(description=bcolors.HEADER + "Easily Block Websites on macOS" + bcolors.ENDC)
	parser.add_argument("-b", dest="block", nargs='+', help="Block a website")
	parser.add_argument("-u", dest="unblock", nargs='+', help="Unblock a wesbite")
	parser.add_argument("-l", dest="ls", action='store_true', help="List blocked websites")

	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	args = parser.parse_args()

	try:
		if args.block:
			for domain_name in args.block:
				block(domain_name)
				if len(domain_name.split(".")) == 2:
					block("www." + domain_name, quiet=True)
				
		if args.unblock:
			for domain_name in args.unblock:
				unblock(domain_name)
				if len(domain_name.split(".")) == 2:
					unblock("www." + domain_name, quiet=True)

		if args.ls:
			list_blocked()
		
	except IOError as error:
		if error.errno != 13:
			raise error
		else:
			print("wguard needs to run as root:\n\n\t %ssudo wguard %s%s\n" % (bcolors.HEADER, " ".join(sys.argv[1:]), bcolors.ENDC))

if __name__ == "__main__":
	main()

