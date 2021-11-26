from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Type, TypeVar

import aiohttp

from .constants import BASE_URL


class ABCSearchParam(ABC):
    @abstractmethod
    def to_string(self) -> str:
        """Convert dataclass to string for API"""


@dataclass
class FieldsSearchParams(ABCSearchParam):
    is_name: bool
    is_author: bool
    is_tags: bool
    is_description: bool

    def to_string(self) -> str:
        params = []

        if self.is_name:
            params.append("NAME")
        if self.is_author:
            params.append("AUTHOR")
        if self.is_tags:
            params.append("TAGS")
        if self.is_description:
            params.append("DESCRIPTION")

        return f"[{','.join(params)}]"


@dataclass
class FunctionsSearchParams(ABCSearchParam):
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

    def to_string(self) -> str:
        params = []

        if self.is_creature:
            params.append("CREATURE")
        if self.is_tribe_creature:
            params.append("TRIBE_CREATURE")
        if self.is_civ_creature:
            params.append("CIV_CREATURE")
        if self.is_space_creature:
            params.append("SPACE_CREATURE")
        if self.is_adventure_creature:
            params.append("ADVENTURE_CREATURE")
        if self.is_city_hall:
            params.append("CITY_HALL")
        if self.is_house:
            params.append("HOUSE")
        if self.is_industry:
            params.append("INDUSTRY")
        if self.is_entertainment:
            params.append("ENTERTAINMENT")
        if self.is_ufo:
            params.append("UFO")
        if self.is_adv_attack:
            params.append("ADV_ATTACK")
        if self.is_adv_collect:
            params.append("ADV_COLLECT")
        if self.is_adv_defend:
            params.append("ADV_DEFEND")
        if self.is_adv_explore:
            params.append("ADV_EXPLORE")
        if self.is_adv_unset:
            params.append("ADV_UNSET")
        if self.is_adv_puzzle:
            params.append("ADV_PUZZLE")
        if self.is_adv_quest:
            params.append("ADV_QUEST")
        if self.is_adv_socialize:
            params.append("ADV_SOCIALIZE")
        if self.is_adv_story:
            params.append("ADV_STORY")
        if self.is_adv_template:
            params.append("ADV_TEMPLATE")

        return f"[{','.join(params)}]"


@dataclass
class ModelsSearchParams(ABCSearchParam):
    is_land: bool
    is_air: bool
    is_water: bool

    def to_string(self) -> str:
        params = []

        if self.is_land:
            params.append("LAND")
        if self.is_air:
            params.append("AIR")
        if self.is_water:
            params.append("WATER")

        return f"[{','.join(params)}]"


@dataclass
class PurposesSearchParams(ABCSearchParam):
    is_military: bool
    is_economic: bool
    is_cultural: bool
    is_colony: bool

    def to_string(self) -> str:
        params = []

        if self.is_military:
            params.append("MILITARY")
        if self.is_economic:
            params.append("ECONOMIC")
        if self.is_cultural:
            params.append("CULTURAL")
        if self.is_colony:
            params.append("COLONY")

        return f"[{','.join(params)}]"


@dataclass
class SearchParams():
    fields: FieldsSearchParams
    functions: FunctionsSearchParams
    models: ModelsSearchParams
    purposes: PurposesSearchParams


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
        filter: str  # TODO: Enum
    ):
        if self._session is None:
            raise ValueError("The session does not exist")

        data = (
            "callCount=1\n"
            "batchId=1\n"
            "scriptSessionId=EEC7AACA9B835CB826C147F3784E3FA2284\n"
            "c0-scriptName=searchService\n"
            "c0-methodName=searchAssetsDWR\n"
            "c0-id=0\n"
            "c0-adv=1\n"
            f"c0-searchText={text}\n"
            f"c0-maxResults={lenght}\n"
            f"c0-filter={filter}\n"
            f"c0-fields={params.fields.to_string()}\n"
            f"c0-functions={params.functions.to_string()}\n"
            f"c0-purposes={params.purposes.to_string()}\n"
            f"c0-modes={params.models.to_string()}\n",
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
            "batchId=1"
        )
        async with self._session.get(
            f"{self._base_url}/jsserv/call/plaincall/searchService.searchAssetsDWR.dwr",
            data=data
        ) as responce:
            # TODO: Check status from `dwr.engine`
            return responce

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
