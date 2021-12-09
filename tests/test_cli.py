import unittest
from unittest.mock import patch, Mock

from asyncclick import BadParameter

from sporepedia import FunctionsSearchParam
from sporepedia.__main__ import BoolDatetimeType


class BoolDatetimeTypeTest(unittest.TestCase):
    def test__no_in_paramets_error(self):
        converter = BoolDatetimeType(FunctionsSearchParam)

        with self.assertRaises(BadParameter):
            converter.convert("123", parameter=None, ctx=None)

    def test__string_split(self):
        converter = BoolDatetimeType(FunctionsSearchParam)

        result = converter.convert(
            "is_city_hall,is_house,is_adv_unset,is_adv_template,",
            parameter=None,
            ctx=None
        )

        self.assertEqual(
            result,
            FunctionsSearchParam(
                is_city_hall=True,
                is_house=True,
                is_adv_unset=True,
                is_adv_template=True,
            )
        )

        result = converter.convert(
            "is_city_hall, is_house ,  is_adv_unset,is_adv_template , ",
            parameter=None,
            ctx=None
        )

        self.assertEqual(
            result,
            FunctionsSearchParam(
                is_city_hall=True,
                is_house=True,
                is_adv_unset=True,
                is_adv_template=True,
            )
        )

        with self.assertRaises(BadParameter):
            converter.convert(
                "is_city_hall|is_house|is_adv_unset|is_adv_template",
                parameter=None,
                ctx=None
            )

    def test__all_string(self):
        converter = BoolDatetimeType(FunctionsSearchParam)

        result = converter.convert("all", parameter=None, ctx=None)

        self.assertEqual(result, FunctionsSearchParam.all())

    def test__none_string(self):
        converter = BoolDatetimeType(FunctionsSearchParam)

        result = converter.convert("none", parameter=None, ctx=None)

        self.assertEqual(result, FunctionsSearchParam.none())
