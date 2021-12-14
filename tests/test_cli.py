import unittest
from unittest.mock import Mock, patch

from asyncclick import BadParameter
from asyncclick.testing import CliRunner

import sporepedia.__main__
from sporepedia.__main__ import (
    BoolDataclassType,
    cli,
)
from sporepedia import FunctionsSearchParam


class BoolDataclassTypeTest(unittest.TestCase):
    def test__no_dataclass_error(self):
        with self.assertRaises(ValueError):
            BoolDataclassType(None)  # type: ignore

    def test__no_in_paramets_error(self):
        converter = BoolDataclassType(FunctionsSearchParam)

        with self.assertRaises(BadParameter):
            converter.convert("123", parameter=None, ctx=None)

    def test__string_split(self):
        converter = BoolDataclassType(FunctionsSearchParam)

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
        converter = BoolDataclassType(FunctionsSearchParam)

        result = converter.convert("all", parameter=None, ctx=None)

        self.assertEqual(result, FunctionsSearchParam.all())

    def test__none_string(self):
        converter = BoolDataclassType(FunctionsSearchParam)

        result = converter.convert("none", parameter=None, ctx=None)

        self.assertEqual(result, FunctionsSearchParam.none())

    def test__get_metavar(self):
        converter = BoolDataclassType(FunctionsSearchParam)

        parameter = Mock()
        result = converter.get_metavar(parameter)

        self.assertEqual(
            result,
            (
                "[is_creature|is_tribe_creature|is_civ_creature"
                "|is_space_creature|is_adventure_creature|is_city_hall"
                "|is_house|is_industry|is_entertainment|is_ufo"
                "|is_adv_attack|is_adv_collect|is_adv_defend"
                "|is_adv_explore|is_adv_unset|is_adv_puzzle|"
                "is_adv_quest|is_adv_socialize|is_adv_story|is_adv_template]"
            )
        )


class TestCommands(unittest.IsolatedAsyncioTestCase):
    async def test__search(self):
        runner = CliRunner()

        with patch.object(sporepedia.__main__.SporepediaClient, "search") as mock:
            mock.return_value.to_json = Mock(
                return_value='{"resultSize": 2668, "results": [], "resultsPerType": {}}'
            )
            result = await runner.invoke(
                cli,
                (
                    "search",
                    "test",
                    "--lenght", "10",
                    "-Fu", "is_creature,is_tribe_creature,is_civ_creature,\
                        is_space_creature,is_adventure_creature,is_city_hall,is_house,\
                        is_industry,is_entertainment,is_ufo,is_adv_attack,is_adv_collect,\
                        is_adv_defend,is_adv_explore,is_adv_unset,is_adv_puzzle,is_adv_quest,\
                        is_adv_socialize,is_adv_story,is_adv_template,",
                    "-F", "most_popular_new",
                    "--fields", "is_name,is_author,is_tag,is_description",
                    "-P", "is_colony",
                )
            )

        self.assertIsNone(result.exception)
        self.assertEqual(
            result.output,
            '{"resultSize": 2668, "results": [], "resultsPerType": {}}\n'
        )
