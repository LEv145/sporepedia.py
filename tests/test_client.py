import unittest
from unittest.mock import AsyncMock, patch
from pathlib import Path

from sporepedia.client import SporepediaClient
from sporepedia.api.client import APIClient


class SporepediaClientTest(unittest.IsolatedAsyncioTestCase):
    @patch.object(APIClient, "request")
    async def test__search(self, mock_request: AsyncMock):
        async with SporepediaClient() as client:
            with open(Path("./tests/testdata/dwr_search_testdata.js")) as fp:
                mock_request.return_value.text.return_value = fp.read()

            await client.search(text="Spore")

    async def test__close_exception(self):
        with self.assertRaises(ValueError):
            await SporepediaClient().close()

    async def test__create_and_close(self):
        client = SporepediaClient()
        await client.create()
        self.assertIsNotNone(client._api)
        await client.close()

        with self.assertRaises(ValueError):
            await SporepediaClient().close()

        async with SporepediaClient() as client:
            self.assertIsInstance(client, SporepediaClient)
            self.assertIsNotNone(client._api)
