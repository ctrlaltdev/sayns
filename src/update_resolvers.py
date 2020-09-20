from pathlib import Path
import requests
import csv
import yaml

class Resolver:
    name = ''
    ip = ''
    country = ''
    reliability = 0
    def __init__(self, ip, name, country = 'WW', reliability = 1):
        self.ip = ip
        self.name = name
        self.country = country
        self.reliability = reliability
    
    def nameserver(self):
        return {
            'ip': self.ip,
            'name': self.name,
            'country': self.country,
            'reliability': self.reliability
        }

def update_resolvers():
    print('Updating resolvers...')

    localresolv = Path('./resolvers.yml')
    tmpfile = Path('/tmp/nameservers.csv')
    ymlfile = Path('.').parent / 'resolvers.yml'

    nameservers = []
    url='https://public-dns.info/nameservers.csv'
    resolvers_csv = requests.get(url)

    open(tmpfile, 'wb').write(resolvers_csv.content)

    with open(tmpfile, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            nameservers.append(Resolver(
                row['ip_address'],
                row['name'] if row['name'] else row['as_org'],
                row['country_code'],
                float(row['reliability'])
            ).nameserver())

    with open(ymlfile, 'w') as file:
        yaml.dump(nameservers, file)

    print('Updated.')
