import json
from typing import cast
import unittest
from pathlib import Path

from sporepedia.api.methods.dwr_parser import (
    SporeDwrEngineParser,
    DwrParserError,
)
from tests.utils.json import json_datetime_hook, json_serial


class SporeDwrEngineParsersTest(unittest.TestCase):

    def test__exception(self):
        parser = SporeDwrEngineParser()

        with open(Path("./tests/testdata/dwr_exception.js")) as fp:
            js_code = fp.read()

        try:
            parser.parse(js_code)
        except Exception as error:
            self.assertIsInstance(error, DwrParserError)
            self.assertEqual(cast(DwrParserError, error).message, "The specified call count is not a number")
            self.assertEqual(cast(DwrParserError, error).name, "org.directwebremoting.extend.ServerException")

    def test__normal(self):
        parser = SporeDwrEngineParser()

        with open(Path("./tests/testdata/dwr_search_testdata.js")) as fp:
            js_code = fp.read()

        with open(Path("./tests/testdata/dwr_search_testdata.json")) as fp:
            result = json.load(fp, object_hook=json_datetime_hook)

        outlog = parser.parse(js_code)

        self.assertEqual(outlog.to_dict(), result)
