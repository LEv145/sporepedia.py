from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import TracebackType, MappingProxyType
from typing import Optional, Type, TypeVar

import aiohttp

from .constants import BASE_URL


class ABCSearchParam(ABC):
    @abstractmethod
    def compose_string(self) -> str:
        """compose dataclass to string for API"""


@dataclass
class FieldsSearchParam(ABCSearchParam):
    is_name: bool
    is_author: bool
    is_tags: bool
    is_description: bool

    def __post_init__(self):
        convert_data = MappingProxyType({
            self.is_name: "name",
            self.is_author: "author",
            self.is_tags: "tags",
            self.is_description: "description"
        })
        self._params = tuple(
            value
            for key, value in convert_data.items()
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class FunctionsSearchParam(ABCSearchParam):
    is_creature: bool
    is_tribe_creature: bool
    is_civ_creature: bool
    is_space_creature: bool
    is_adventure_creature: bool
    is_city_hall: bool
    is_house: bool
    is_industry: bool
    is_entertainment: bool
    is_ufo: bool
    is_adv_attack: bool
    is_adv_collect: bool
    is_adv_defend: bool
    is_adv_explore: bool
    is_adv_unset: bool
    is_adv_puzzle: bool
    is_adv_quest: bool
    is_adv_socialize: bool
    is_adv_story: bool
    is_adv_template: bool

    def __post_init__(self):
        convert_data = MappingProxyType({
            self.is_creature: "CREATURE",
            self.is_tribe_creature: "TRIBE_CREATURE",
            self.is_civ_creature: "CIV_CREATURE",
            self.is_space_creature: "SPACE_CREATURE",
            self.is_adventure_creature: "ADVENTURE_CREATURE",
            self.is_city_hall: "CITY_HALL",
            self.is_house: "HOUSE",
            self.is_industry: "INDUSTRY",
            self.is_entertainment: "ENTERTAINMENT",
            self.is_ufo: "UFO",
            self.is_adv_attack: "ADV_ATTACK",
            self.is_adv_collect: "ADV_COLLECT",
            self.is_adv_defend: "ADV_DEFEND",
            self.is_adv_explore: "ADV_EXPLORE",
            self.is_adv_explore: "ADV_EXPLORE",
            self.is_adv_unset: "ADV_UNSET",
            self.is_adv_puzzle: "ADV_PUZZLE",
            self.is_adv_quest: "ADV_QUEST",
            self.is_adv_socialize: "ADV_SOCIALIZE",
            self.is_adv_story: "ADV_STORY",
            self.is_adv_template: "ADV_TEMPLATE",
        })
        self._params = tuple(
            value
            for key, value in convert_data.items()
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class ModelsSearchParam(ABCSearchParam):
    is_land: bool
    is_air: bool
    is_water: bool

    def __post_init__(self):
        convert_data = MappingProxyType({
            self.is_land: "LAND",
            self.is_air: "AIR",
            self.is_water: "WATER",
        })
        self._params = tuple(
            value
            for key, value in convert_data.items()
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class PurposesSearchParam(ABCSearchParam):
    is_military: bool
    is_economic: bool
    is_cultural: bool
    is_colony: bool

    def __post_init__(self):
        convert_data = MappingProxyType({
            self.is_military: "MILITARY",
            self.is_economic: "ECONOMIC",
            self.is_cultural: "CULTURAL",
            self.is_colony: "COLONY",
        })
        self._params = tuple(
            value
            for key, value in convert_data.items()
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class SearchParams():
    fields: FieldsSearchParam
    functions: FunctionsSearchParam
    models: ModelsSearchParam
    purposes: PurposesSearchParam


class APIClient():
    """
    Low level api
    """
    APIClientType = TypeVar("APIClientType", bound="APIClient")

    _base_url: str = BASE_URL

    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None

    async def create(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self._session = (
            aiohttp.ClientSession()
            if session is None else
            session
        )

    async def __aenter__(
        self: "APIClientType",
        session: Optional[aiohttp.ClientSession] = None
    ) -> "APIClientType":
        await self.create(session)
        return self

    async def search(
        self,
        text: str,
        lenght: int,
        params: SearchParams,
        filter: str,  # TODO: Enum
        batch_id: int = 1,
        adv: int = 1
    ):
        data = (
            "callCount=1\n"
            "scriptSessionId=EEC7AACA9B835CB826C147F3784E3FA2284\n"
            "c0-scriptName=searchService\n"
            "c0-methodName=searchAssetsDWR\n"
            "c0-id=0\n"
            f"c0-adv={adv}\n"
            f"c0-searchText={text}\n"
            f"c0-maxResults={lenght}\n"
            f"c0-filter={filter}\n"
            f"c0-fields={params.fields.compose_string()}\n"
            f"c0-functions={params.functions.compose_string()}\n"
            f"c0-purposes={params.purposes.compose_string()}\n"
            f"c0-modes={params.models.compose_string()}\n",
            "c0-param0=Object_Object:{"
                "adv:reference:c0-adv, "  # noqa: E131
                "searchText:reference:c0-searchText, "
                "maxResults:reference:c0-maxResults, "
                "fields:reference:c0-fields, "
                "functions:reference:c0-functions, "
                "purposes:reference:c0-purposes, "
                "modes:reference:c0-modes, "
                "filter:reference:c0-filter "
            "}\n"
            f"batchId={batch_id}"
        )
        responce = await self._request(
            f"{self._base_url}/jsserv/call/plaincall/searchService.searchAssetsDWR.dwr",
            data=data
        )
        return responce

    async def _request(self, *args, **kw) -> str:
        if self._session is None:
            raise ValueError("The session does not exist")

        responce = await self._session.get(*args, **kw)
        responce.raise_for_status()
        return (
            await responce.text()
        )

    async def close(self) -> None:
        if self._session is None:
            raise ValueError("The session does not exist")

        await self._session.close()

    async def __aexit__(
        self,
        _exception_type: Type[BaseException],
        _exception: BaseException,
        _traceback: TracebackType
    ) -> None:
        await self.close()
