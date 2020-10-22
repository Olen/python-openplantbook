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

    async def get_plantbook_token(self):
        """Get the token from the openplantbook API."""
        if not self.client_id or not self.secret:
            return False
        self.token = None
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

        except Exception:  # pylint: disable=broad-except
            _LOGGER.error("Unable to connect to openplantbook")
            raise


    async def get_plantbook_data(self, species):
        """Get information about the plant from the openplantbook API."""
        if not self.token:
            _LOGGER.debug("No plantbook token. Trying to get one")
            await self.get_plantbook_token()
            if not self.token:
                _LOGGER.error("Unable to get plantbook token")
                return
        expires = datetime.fromisoformat(self.token.get('expires'))
        if expires < datetime.now() + timedelta(hours=1):
            _LOGGER.debug("Expiring plantbook token, renewing")
            await self.get_plantbook_token()
            if not token:
                _LOGGER.error("Unable to renew plantbook token")
                return

        url = f"{PLANTBOOK_BASEURL}/plant/detail/{species}"
        headers = {
            "Authorization": f"Bearer {self.token.get('access_token')}"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as result:
                    _LOGGER.debug("Fetched data from %s", url)
                    res = await result.json()
                    return res
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Unable to get plant from plantbook API: %s", str(exception))
        return False


