import json
import unittest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from pathlib import Path

from tests.utils.datetime import validate_dataclass
from tests.utils.json import json_datetime_hook

from sporepedia.api.client import APIClient
from sporepedia.api.methods.mixins.search import (
    SearchResponceBuilder,
    SearchRequestComposer,
    SearchParams,
    FieldsSearchParam,
    FunctionsSearchParam,
    ModelsSearchParam,
    PurposesSearchParam,
    SearchFilter,
    SearchServiceResult,
    Creation,
    Author,
    AdventureStat,
    Status,
    StatusName,
    Difficulty,
    builders,
)


class SearchParamTest(unittest.TestCase):

    def test__all(self):
        params = SearchParams(
            fields=FieldsSearchParam.all(),
            functions=FunctionsSearchParam.all(),
            models=ModelsSearchParam.all(),
            purposes=PurposesSearchParam.all(),
        )

        dataclasses = (
            params.guaranteed_fields,
            params.guaranteed_functions,
            params.guaranteed_models,
            params.guaranteed_purposes,
        )

        for dataclass_ in dataclasses:
            for name, _ in dataclass_.__dataclass_fields__.items():
                self.assertEqual(getattr(dataclass_, name), True)

    def test__none(self):
        params = SearchParams(
            fields=FieldsSearchParam.none(),
            functions=FunctionsSearchParam.none(),
            models=ModelsSearchParam.none(),
            purposes=PurposesSearchParam.none(),
        )

        dataclasses = (
            params.guaranteed_fields,
            params.guaranteed_functions,
            params.guaranteed_models,
            params.guaranteed_purposes,
        )

        for dataclass_ in dataclasses:
            for name, _ in dataclass_.__dataclass_fields__.items():
                self.assertEqual(getattr(dataclass_, name), False)


class MethodsTest(unittest.IsolatedAsyncioTestCase):
    @patch.object(APIClient, "request")
    async def test__search(self, mock_request: AsyncMock):
        self._client = APIClient()

        with open(Path("./tests/testdata/dwr_search_testdata.js")) as fp:
            mock_request.return_value.text.return_value = fp.read()

        async with self._client as client:
            result = await client.search(
                text="test",
                lenght=20,
                params=SearchParams(
                    fields=FieldsSearchParam(
                        is_name=True,
                        is_author=True,
                        is_tag=True,
                    ),
                    functions=FunctionsSearchParam(
                        is_tribe_creature=True,
                        is_adventure_creature=True,
                        is_industry=True,
                        is_adv_collect=True,
                        is_adv_puzzle=True,
                        is_adv_template=True
                    ),
                    purposes=PurposesSearchParam(
                        is_military=True,
                        is_cultural=True,
                    ),
                ),
                filter=SearchFilter.featured,
                batch_id=4,
                adv=2
            )

        self.assertEqual(
            result,
            SearchServiceResult(
                result_size=1,
                results=[
                    Creation(
                        id=500377997389,
                        original_id=500377997764,
                        parent_id=500377997764,
                        rating=14.376374,
                        name="The Psychic Planet",
                        type="ADVENTURE",
                        description=(
                            "A psychic entity has you at its disposal. What will it have you do? "
                            "Now actually working! Thanks for making this a rising star guys.EDIT: I haven't "
                            "checked out this in a while! Thanks for making this on the TOP PAGE! "
                        ),
                        images_count=2,
                        thumbnail_size=41862,
                        source_ip="98.203.139.225",
                        locale_string="en_US",
                        required_products=["EXPANSION_PACK1", "INSECT_LIMBS", "SPORE_CORE"],
                        tags=["cool", "fun", "lava", "psychic", "puzzle", "test"],
                        audit_trail=None,
                        asset_id=500377997389,
                        asset_function="ADV_PUZZLE",
                        is_quality=True,
                        create_at=datetime(2009, 6, 26, 16, 55, 48),
                        update_at=datetime(2016, 4, 28, 15, 45, 14),
                        feature_at=datetime(2009, 7, 8, 0, 0),
                        author=Author(
                            id=2262951433,
                            user_id=2262951433,
                            nucleus_user_id=2262951433,
                            persona_id=173842184,
                            name="Doomwaffle",
                            screen_name="Doomwaffle",
                            avatar_image="https://www.spore.com/static/thumb/500/335/938/500335938963.png",
                            tagline="Galactic Adventurer",
                            assets_count=128,
                            subscriptions_count=359,
                            is_default=True,
                            is_custom_avatar_image=False,
                            create_at=datetime(2008, 6, 18, 1, 57),
                            newest_asset_create_at=datetime(2012, 3, 22, 21, 23),
                            update_at=datetime(2009, 6, 26, 4, 19, 36),
                            last_login_at=datetime(2012, 5, 25, 0, 52, 5),
                        ),
                        adventure_stat=AdventureStat(
                            id=500377997389,
                            leaderboard_id=500377997389,
                            difficulty=Difficulty(5),
                            locked_captain_asset_id=None,
                            plays_count=157748,
                            losses_count=104177,
                            wins_count=53571,
                            points_count=51,
                            update_at=datetime(2013, 6, 18, 18, 13, 21),
                        ),
                        status=Status(
                            name=StatusName("CLASSIFIED"),
                            name_key="asset.status.classified",
                            declaring_class_name="com.ea.sp.pollinator.db.Asset$Status",
                        ),
                    )
                ],
            )
        )


class ResponceBuilderTest(unittest.TestCase):
    def setUp(self):
        self._builder = SearchResponceBuilder()

    def test(self):
        with open(Path("./tests/testdata/dwr_1000creation_search_result.js")) as fp:
            js_code = fp.read()

        with open(Path("./tests/testdata/dwr_1000creation_search_result.json")) as fp:
            data = json.load(fp, object_hook=json_datetime_hook)

        with patch.object(
            builders,
            "parse_dwr",
        ) as mock:
            mock.return_value.to_dict.return_value = data
            result = self._builder.build(js_code)

        for creation in result.results:
            validate_dataclass(creation)


class RequestComposerTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._composer = SearchRequestComposer()

    async def test__min_data(self):
        result = self._composer.compose(
            text="Toster1",
            lenght=1,
            params=SearchParams(),
            filter=None,
            batch_id=3,
            adv=1,
            session_id="B46A8740BB941667AB32B719F1B7115A19",
        )

        self.assertEqual(
            result,
            """callCount=1
scriptSessionId=B46A8740BB941667AB32B719F1B7115A19
c0-scriptName=searchService
c0-methodName=searchAssetsDWR
c0-id=0
c0-adv=1
c0-searchText=Toster1
c0-maxResults=1
c0-filter=NONE
c0-fields=[]
c0-functions=[]
c0-purposes=[]
c0-modes=[]
c0-param0=Object_Object:{adv:reference:c0-adv, searchText:reference:c0-searchText, \
maxResults:reference:c0-maxResults, fields:reference:c0-fields, \
functions:reference:c0-functions, purposes:reference:c0-purposes, \
modes:reference:c0-modes, filter:reference:c0-filter }
batchId=3""",
        )

    async def test__max_data(self):
        result = self._composer.compose(
            text="Toster2",
            lenght=1,
            params=SearchParams(
                fields=FieldsSearchParam.all(),
                functions=FunctionsSearchParam.all(),
                models=ModelsSearchParam.all(),
                purposes=PurposesSearchParam.all(),
            ),
            filter=SearchFilter.featured,
            batch_id=2,
            adv=0,
            session_id="B46A8740BB941667AB32B719F1B7115A18"
        )

        self.assertEqual(
            result,
            """callCount=1
scriptSessionId=B46A8740BB941667AB32B719F1B7115A18
c0-scriptName=searchService
c0-methodName=searchAssetsDWR
c0-id=0
c0-adv=0
c0-searchText=Toster2
c0-maxResults=1
c0-filter=FEATURED
c0-fields=[name,author,tags,description]
c0-functions=[CREATURE,TRIBE_CREATURE,CIV_CREATURE,\
SPACE_CREATURE,ADVENTURE_CREATURE,CITY_HALL,HOUSE,INDUSTRY,\
ENTERTAINMENT,UFO,ADV_ATTACK,ADV_COLLECT,ADV_DEFEND,ADV_EXPLORE,\
ADV_EXPLORE,ADV_UNSET,ADV_PUZZLE,ADV_QUEST,ADV_SOCIALIZE,\
ADV_STORY,ADV_TEMPLATE]
c0-purposes=[MILITARY,ECONOMIC,CULTURAL,COLONY]
c0-modes=[LAND,AIR,WATER]
c0-param0=Object_Object:{adv:reference:c0-adv, searchText:reference:c0-searchText, \
maxResults:reference:c0-maxResults, fields:reference:c0-fields, \
functions:reference:c0-functions, purposes:reference:c0-purposes, \
modes:reference:c0-modes, filter:reference:c0-filter }
batchId=2""",
        )
