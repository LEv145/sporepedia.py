import unittest
from pathlib import Path

from sporepedia.builders import SearchResponceBuilder


class SearchResponceBuilderTest(unittest.TestCase):
    def setUp(self):
        self._builder = SearchResponceBuilder()

    async def test_search(self):
        with open(Path("./tests/testdata/dwr_1000creation_search_result.js")) as fp:
            js_code = fp.read()

        result = self._builder.build(js_code)
