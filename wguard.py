#!/usr/bin/env python

import argparse
import sys

hosts_file_path = "/etc/hosts"
ipv4_block_address = "127.0.0.1"
ipv6_block_address = "::1"

def is_blocked_entry(hosts_file_line):
	line_parts = hosts_file_line.split()
	if len(line_parts) != 2: return False
	is_blocked_ipv4 = line_parts[0] == ipv4_block_address
	is_blocked_ipv6 = line_parts[0] == ipv6_block_address
	is_domain_localhost = line_parts[1] == "localhost"
	return (is_blocked_ipv4 or is_blocked_ipv6) and not is_domain_localhost

def list_blocked():
	blocked = set()
	with open(hosts_file_path, 'r') as hosts_file:
		for hosts_file_line in hosts_file.read().splitlines():
			if is_blocked_entry(hosts_file_line):
				domain_name = hosts_file_line.split()[1]
				if domain_name.startswith("www."):
					blocked.add(domain_name[4:])
				else:
					blocked.add(domain_name)
	for domain_name in blocked:
		print(domain_name)
	
	
def block(domain_name):
	domain_name_parts = domain_name.split(".")
	to_block = [domain_name]
	if len(domain_name_parts) == 2:
		to_block.append("www." + domain_name)
	new_entries = list(map(lambda x: "%-15s %s\n%-15s %s\n" % (ipv4_block_address, x, ipv6_block_address, x), to_block))
	with open(hosts_file_path, "r") as hosts_file:
		current_hosts_file_contents = hosts_file.read()
	with open(hosts_file_path, "a") as hosts_file:
		if current_hosts_file_contents[-1] != "\n":
			hosts_file.write("\n")
		for new_entry in new_entries:
			hosts_file.write(new_entry)

def unblock(domain_name):
	lines_to_remove = []
	with open(hosts_file_path, 'r') as hosts_file:
		hosts_file_lines = hosts_file.read().splitlines()
	with open(hosts_file_path, 'w') as hosts_file:
		for hosts_file_line in hosts_file_lines:
			if is_blocked_entry(hosts_file_line):
				blocked_domain = hosts_file_line.split()[1]
				if blocked_domain == domain_name or blocked_domain == "www." + domain_name:
					continue
			hosts_file.write(hosts_file_line + "\n")
	

parser = argparse.ArgumentParser(description="Easily block websites on Mac")
args_group = parser.add_mutually_exclusive_group()
args_group.add_argument("-b", dest="block", nargs='+', help="Block a website")
args_group.add_argument("-u", dest="unblock", nargs='+', help="Unblock a wesbite")
args_group.add_argument("-l", dest="ls", action='store_true', help="List blocked websites")

if len(sys.argv) == 1:
	parser.print_help(sys.stderr)
	sys.exit(1)

args = parser.parse_args()

try:
	if args.ls:
		list_blocked()
	elif args.block:
		for domain_name in args.block:
			block(domain_name)
	elif args.unblock:
		for domain_name in args.unblock:
			unblock(domain_name)
except IOError as error:
	if error.errno != 13:
		raise error
	else:
		print("wguard was unable to write to your hosts file; try running it with sudo.")

