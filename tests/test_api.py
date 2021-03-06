import unittest
from unittest.mock import patch, Mock

from aiohttp import ClientSession

from sporepedia.api.client import APIClient


class APITest(unittest.IsolatedAsyncioTestCase):
    async def test__api_request(self):
        client = APIClient()

        with self.assertRaises(ValueError):
            await client.request("POST", "https://spore.com")

        await client.create()

        with patch.object(ClientSession, "_request") as request:
            request.return_value.raise_for_status = Mock(return_value=None)
            await client.request("POST", "https://spore.com")

        await client.close()

    async def test__create_and_close(self):
        client = APIClient()

        await client.create()
        await client.close()

        with self.assertRaises(ValueError):
            await APIClient().close()

        async with APIClient() as client:
            self.assertIsInstance(client, APIClient)
