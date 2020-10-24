#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

import asyncio
import sys
import yaml
from tabulate import tabulate

from pyopenplantbook import OpenPlantBookApi, MissingClientIdOrSecret

ALIAS="Capsicum"

try:
    with open(r'config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError:
    print("Config-file not found.")
    print("Copy config.yaml.dist to config.yaml and add client_id and secret from https://open.plantbook.io/apikey/show/")
    sys.exit()
except Exception as e:
    print(e)
    sys.exit()

api = OpenPlantBookApi(config['client_id'], config['secret'])

print(f"Searching the OpenPlantbook for {ALIAS}...")

try:
    res = asyncio.run(api.search_plantbook(ALIAS))
except MissingClientIdOrSecret:
    print("Missing or invalid client id or secret")
    sys.exit()
except Exception as e:
    print(e)
    sys.exit()

print("Found:")
print(tabulate(res['results'], headers={'pid': 'PID', 'display_pid': 'Display PID', 'alias': 'Alias'}, tablefmt="psql"))
print("{} plants found".format(len(res['results'])))


print("Getting details for a single plant...")

try:
    plant = res['results'][0]
    res = asyncio.run(api.get_plantbook_data(plant['pid']))
    print("Found:")
    print(tabulate(res.items(), headers=['Key', 'Value'], tablefmt="psql"))

except Exception as e:
    print(e)
    sys.exit()
