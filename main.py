#!python3
import json
import sys
import os
import netifaces
import requests

# CONSTS
SUCCESS = 0
# error codes
ARGV_ERROR = 1
NONE_ZONE_ID = 2

# global variable
zone_id = None

def get_interface_ip(config):
    addresses = netifaces.ifaddresses(config['interface'])
    return addresses[netifaces.AF_INET][0]['addr']

def main():
    if len(sys.argv) < 2:
        print("plz look read manural first")
        sys.exit(ARGV_ERROR)
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("# gandi-ddns")
        print("just run ./main.py config.json")
        sys.exit(SUCCESS)
    with open(sys.argv[1]) as config_file:
        data = json.load(config_file)
        record_url = 'https://api.gandi.net/v5/livedns/domains/' + data['domain'] + '/records'
        update_url = 'https://api.gandi.net/v5/livedns/domains/'+data['domain']+'/records/'+data['record_name']+'/' + data['record_type']

        auth_header = {
            'authorization': 'Apikey '+data['apikey']
        }

        record_params = {
            'fqdn': data['domain']
        }
        update_params = {
            'fqdn': data['domain'],
            'rrset_name': data['record_name'],
            'rrset_type': data['record_type']
        }

        update_body = {
            'rrset_values': [
                get_interface_ip(data)
            ],
            'rrset_ttl': data['ttl']
        }

        update_response = requests.request(
            "PUT",
            update_url,
            params = update_params,
            headers = auth_header,
            data = json.dumps(
                update_body
            )
        )

        response = requests.request(
            "GET",
            record_url,
            params = record_params,
            headers = auth_header,
        )
        print(response.text)

if __name__ == '__main__':
    main()

