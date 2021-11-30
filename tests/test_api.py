import aiounittest

from unittest.mock import patch

from sporepedia import api
from sporepedia.api import APIClient
from sporepedia.enums import SearchFilter


class APITest(aiounittest.AsyncTestCase):

    def setUp(self):
        self._client = APIClient()

    @staticmethod
    def _request(method: str, *args, **kw):  # FIXME: Test
        return 1

    @patch("sporepedia.api.APIClient._request", return_value=9)  # FIXME: Test
    async def test_search(self, mock_requests):
        async with self._client as client:
            result = await client.search(
                text="test",
                lenght=20,
                params=api.SearchParams(
                    fields=api.FieldsSearchParam(
                        is_name=True,
                        is_author=True,
                        is_tag=True,
                    ),
                    functions=api.FunctionsSearchParam(
                        is_tribe_creature=True,
                        is_adventure_creature=True,
                        is_industry=True,
                        is_adv_collect=True,
                        is_adv_puzzle=True,
                        is_adv_template=True
                    ),
                    purposes=api.PurposesSearchParam(
                        is_military=True,
                        is_cultural=True,
                    ),
                ),
                filter=SearchFilter.featured,
                batch_id=4,
                adv=2
            )
        print(result)
