import unittest
from unittest.mock import AsyncMock, patch
from pathlib import Path
from datetime import datetime

from sporepedia.api.client import (
    APIClient,
    SearchParams,
    FieldsSearchParam,
    FunctionsSearchParam,
    PurposesSearchParam,
    SearchFilter,
    SearchServiceResult,
)
from sporepedia.api.models import (
    Creation,
    Author,
    AdventureStat,
    Status,
    StatusName,
)


class APITest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._client = APIClient()

    @patch.object(APIClient, "_request")
    async def test_search(self, mock_request: AsyncMock):
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
                            difficulty=5,
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
