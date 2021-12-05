import pickle
import unittest
from unittest.mock import patch
from pathlib import Path

from tests.utils import validate_dataclass
import sporepedia.api.builders
from sporepedia.api.builders import SearchResponceBuilder


class SearchResponceBuilderTest(unittest.TestCase):
    def setUp(self):
        self._builder = SearchResponceBuilder()

    def test(self):
        with open(Path("./tests/testdata/dwr_1000creation_search_result.js")) as fp:
            js_code = fp.read()

        with open(Path("./tests/testdata/dwr_1000creation_search_result.pickle"), "rb") as fp:
            data = pickle.loads(fp.read())

        with patch.object(
            sporepedia.api.builders,
            "parse_dwr",
        ) as mock:
            mock.return_value.to_dict.return_value = data
            result = self._builder.build(js_code)

        for creation in result.results:
            validate_dataclass(creation)
