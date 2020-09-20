#!/usr/bin/env python3

import sys
import getopt
import yaml
import dns.resolver
from pathlib import Path
from src import update_resolvers, create_resolver

print()
print('███████╗ █████╗ ██╗   ██╗███╗   ██╗███████╗')
print('██╔════╝██╔══██╗╚██╗ ██╔╝████╗  ██║██╔════╝')
print('███████╗███████║ ╚████╔╝ ██╔██╗ ██║███████╗')
print('╚════██║██╔══██║  ╚██╔╝  ██║╚██╗██║╚════██║')
print('███████║██║  ██║   ██║   ██║ ╚████║███████║')
print('╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝')
print()

ymlfile = Path('./resolvers.yml')
resolvers = []

def get_records (domain, dns_type, resolver):
    resolv = []
    
    try:
        records = resolver.resolve(domain, dns_type)
        for data in records:
            resolv.append(data)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        resolv.append('-')

def print_usage(status = 0):
    print('sayns -d <domain.tld> -t <DNS type>')
    sys.exit(status)

def main(argv):
    domain = None
    dns_type = None
    countries = []

    try:
        opts, args = getopt.getopt(argv,'hud:t:c:')
    except getopt.GetoptError:
        print_usage(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
        elif opt in ('-u', '--update-resolvers'):
            update_resolvers()
            exit(0)
        elif opt in ('-d', '--domain'):
            domain = arg
        elif opt in ('-t', '--dns_type'):
            dns_type = arg
        elif opt in ('-c', '--country'):
            countries.append(arg)
    
    if domain == None or dns_type == None:
        print_usage(2)

    with open(ymlfile) as file:
        resolvers = yaml.load(file, Loader=yaml.FullLoader)

    if len(countries) > 0:
        resolvers = [r for r in resolvers if r.country in countries]

    print(resolvers)
    exit(0)

    for resolver in resolvers:
        resolv = create_resolver(resolver)
        get_records(domain, dns_type, resolv)

if __name__ == '__main__':
    main(sys.argv[1:])
