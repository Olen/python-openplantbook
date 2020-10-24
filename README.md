# OpenPlantbook
Open Plantbook is a free service to access plant data. Anyone can use information from the database for any purpose without limitations.



## Requrements
In order to use this API you need to login to Open Plantbook web UI at https://open.plantbook.io and generate API credentials. The credentials are client_id and client_secret. API authentication implements OAuth2 standard Client Credentials Grant flow.

## Usage

The library is written with async functions.


```
import asyncio

from pyopenplantbook import OpenPlantBookApi

client_id = "xxxx"
secret = "yyyy"

api = OpenPlantBookApi(client_id=client_id, secret=secret)

async def get_plant(species):
    plant = await api.get_plantbook_data(species=species)
    return plant

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(get_plant("coleus 'marble'"))
    print(result)

main()
```
