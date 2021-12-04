import unittest

from sporepedia.api import (
    SearchParams,
    FieldsSearchParam,
    ModelsSearchParam,
    PurposesSearchParam,
    FunctionsSearchParam,
    SearchFilter,
)
from sporepedia.composers import SearchRequestComposer


class SearchRequestComposerTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._composer = SearchRequestComposer()

    async def test_min_data(self):
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

    async def test_max_data(self):
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
