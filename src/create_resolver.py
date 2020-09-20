import re
import dns.resolver

def create_resolver(resolv):
    resolve_ip = []

    patv4 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    isIPv4 = patv4.match(resolv)

    if isIPv4:
        resolve_ip = [resolv]
    else:
        records = dns.resolver.resolve(resolv, 'A')
        for data in records:
            resolve_ip.append(str(data))

    new_resolver = dns.resolver.Resolver()
    new_resolver.nameservers = resolve_ip
    return new_resolver
