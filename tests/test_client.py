import unittest
from unittest.mock import AsyncMock, patch
from pathlib import Path

from sporepedia.api import APIClient
from sporepedia.client import SporepediaClient
from sporepedia.models import SearchServiceResult


class APITest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._client = SporepediaClient()

    @patch.object(APIClient, "_request")
    async def test_search(self, mock_request: AsyncMock):
        with open(Path("./tests/testdata/dwr_search_testdata.js")) as fp:
            mock_request.return_value.text.return_value = fp.read()

        result = await self._client.search(text="Spore")
        self.assertIsInstance(result, SearchServiceResult)
