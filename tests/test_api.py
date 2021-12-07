import unittest
from unittest.mock import patch

from aiohttp import ClientSession

from sporepedia.api.client import APIClient


class APITest(unittest.IsolatedAsyncioTestCase):
    async def test_api_request(self):
        client = APIClient()

        with self.assertRaises(ValueError):
            await client.request("POST", "https://spore.com")

        await client.create()

        with patch.object(ClientSession, "_request") as request:
            request.return_value.ok = True  # TODO
            await client.request("POST", "https://spore.com")

        await client.close()

    async def test_create_and_close(self):
        client = APIClient()

        await client.create()
        await client.close()

        with self.assertRaises(ValueError):
            await APIClient().close()

        async with APIClient() as client:
            self.assertIsInstance(client, APIClient)
