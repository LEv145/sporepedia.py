from typing import cast
import unittest
from pathlib import Path

from sporepedia.errors import DwrParserError
from sporepedia.dwr_parser import SporeDwrEngineParser


class SporeDwrEngineParsersTest(unittest.TestCase):

    def test_exception(self):
        parser = SporeDwrEngineParser()

        with open(Path("./tests/testdata/dwr_exception.js")) as fp:
            js_code = fp.read()

        try:
            parser.parse(js_code)
        except Exception as error:
            self.assertIsInstance(error, DwrParserError)
            self.assertEqual(cast(DwrParserError, error).message, "The specified call count is not a number")
            self.assertEqual(cast(DwrParserError, error).name, "org.directwebremoting.extend.ServerException")

    def test_normal(self):
        parser = SporeDwrEngineParser()

        with open(Path("./tests/testdata/dwr_search_testdata.js")) as fp:
            js_code = fp.read()

        outlog = parser.parse(js_code)

        self.assertEqual(  # TODO: How test JsObjectWrapper
            outlog.to_dict()["resultSize"],
            1
        )
