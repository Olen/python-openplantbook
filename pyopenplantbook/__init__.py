#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:


import aiohttp
import logging
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

PLANTBOOK_BASEURL = "https://open.plantbook.io/api/v1"


class OpenPlantBookApi:
    """Fetches data from the OpenPlantbook API."""

    def __init__(self, client_id, secret):
        """Initialize."""
        self.token = None
        self.client_id = client_id
        self.secret = secret



    async def get_plantbook_data(self, species):
        """Get information about the plant from the openplantbook API."""
        try: 
            await self._get_plantbook_token()
        except Exception:
            _LOGGER.error("No plantbook token")
            raise

        url = f"{PLANTBOOK_BASEURL}/plant/detail/{species}"
        headers = {
            "Authorization": f"Bearer {self.token.get('access_token')}"
        }
        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.get(url, headers=headers) as result:
                    _LOGGER.debug("Fetched data from %s", url)
                    res = await result.json()
                    return res
        except aiohttp.ServerTimeoutError:
            # Maybe set up for a retry, or continue in a retry loop
            _LOGGER.error("Timeout connecting to {}".format(url))
            return None
        except aiohttp.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            _LOGGER.error("Too many redirects connecting to {}".format(url))
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(err)
            return None
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Unable to get plant from plantbook API: %s", str(exception))
            return None
        return None


    async def search_plantbook(self, alias):
        """Search the openplantbook API."""
        try: 
            await self._get_plantbook_token()
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error("No plantbook token")
            raise

        url = f"{PLANTBOOK_BASEURL}/plant/search?limit=1000&alias={alias}"
        headers = {
            "Authorization": f"Bearer {self.token.get('access_token')}"
        }
        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.get(url, headers=headers) as result:
                    _LOGGER.debug("Fetched data from %s", url)
                    res = await result.json()
                    return res
        except aiohttp.ServerTimeoutError:
            # Maybe set up for a retry, or continue in a retry loop
            _LOGGER.error("Timeout connecting to {}".format(url))
            return None
        except aiohttp.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            _LOGGER.error("Too many redirects connecting to {}".format(url))
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(err)
            return None
        return None




    async def _get_plantbook_token(self):
        """Get the token from the openplantbook API."""
        if not self.client_id or not self.secret:
            raise MissingClientIdOrSecret
        if self.token:
            expires = datetime.fromisoformat(self.token.get('expires'))
            if expires > datetime.now() + timedelta(hours=1):
                _LOGGER.debug("Token is still valid")
                return True

        url = f"{PLANTBOOK_BASEURL}/token/"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.secret,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as result:
                    token = await result.json()
                    if token.get("access_token"):
                        _LOGGER.debug("Got token from %s", url)
                        token["expires"] = (datetime.now() + timedelta(seconds=token["expires_in"])).isoformat()
                        self.token = token
                        return True
                    raise PermissionError
        except PermissionError:
            _LOGGER.error("Wrong client id or secret")
            return None
        except aiohttp.ServerTimeoutError:
            # Maybe set up for a retry, or continue in a retry loop
            _LOGGER.error("Timeout connecting to {}".format(url))
            return None
        except aiohttp.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            _LOGGER.error("Too many redirects connecting to {}".format(url))
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(err)
            return None

        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.error("Unable to connect to openplantbook: %s", str(e))
            raise

class MissingClientIdOrSecret(Exception):
    """Exception for missing client_id or token."""
    pass
