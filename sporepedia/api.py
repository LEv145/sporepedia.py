from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Type, TypeVar

import aiohttp

from sporepedia.enums import SearchFilter

from .builders import SearchServiceBuilder
from .constants import BASE_URL


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

    async def search(
        self,
        text: str,
        lenght: int,
        params: "SearchParams",
        filter: Optional[SearchFilter],
        batch_id: int = 1,
        adv: int = 1,
    ):
        _filter = (
            "NONE"
            if filter is None else
            filter.value
        )

        data = (
            "callCount=1\n"
            "scriptSessionId=B46A8740BB941667AB32B719F1B7115A19\n"
            "c0-scriptName=searchService\n"
            "c0-methodName=searchAssetsDWR\n"
            "c0-id=0\n"
            f"c0-adv={adv}\n"
            f"c0-searchText={text}\n"
            f"c0-maxResults={lenght}\n"
            f"c0-filter={_filter}\n"
            f"c0-fields={params._fields.compose_string()}\n"
            f"c0-functions={params._functions.compose_string()}\n"
            f"c0-purposes={params._purposes.compose_string()}\n"
            f"c0-modes={params._models.compose_string()}\n"
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

        response = await self._request(
            method="POST",
            url=f"{self._base_url}/jsserv/call/plaincall/searchService.searchAssetsDWR.dwr",
            data=data,
        )

        builder = SearchServiceBuilder()
        return builder.build(await response.text())

    async def close(self) -> None:
        if self._session is None:
            raise ValueError("The session does not exist")

        await self._session.close()

    async def _request(self, method: str, url: str, *args, **kw) -> aiohttp.ClientResponse:
        if self._session is None:
            raise ValueError("The session does not exist")

        response = await self._session.request(
            url=url,
            method=method,
            *args, **kw
        )
        response.raise_for_status()
        return response

    async def __aenter__(
        self: "APIClientType",
        session: Optional[aiohttp.ClientSession] = None
    ) -> "APIClientType":
        await self.create(session)
        return self

    async def __aexit__(
        self,
        _exception_type: Type[BaseException],
        _exception: BaseException,
        _traceback: TracebackType,
    ) -> None:
        await self.close()


class ABCSearchParam(ABC):
    @abstractmethod
    def compose_string(self) -> str:
        """compose dataclass to string for API"""


@dataclass
class FieldsSearchParam(ABCSearchParam):
    # FIXME: Alignment?
    is_name: bool = False
    is_author: bool = False
    is_tag: bool = False
    is_description: bool = False

    def __post_init__(self):
        convert_data = (
            (self.is_name, "name"),
            (self.is_author, "author"),
            (self.is_tag, "tags"),
            (self.is_description, "description"),
        )
        self._params = tuple(
            value
            for key, value in convert_data
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class FunctionsSearchParam(ABCSearchParam):
    is_creature: bool = False
    is_tribe_creature: bool = False
    is_civ_creature: bool = False
    is_space_creature: bool = False
    is_adventure_creature: bool = False
    is_city_hall: bool = False
    is_house: bool = False
    is_industry: bool = False
    is_entertainment: bool = False
    is_ufo: bool = False
    is_adv_attack: bool = False
    is_adv_collect: bool = False
    is_adv_defend: bool = False
    is_adv_explore: bool = False
    is_adv_unset: bool = False
    is_adv_puzzle: bool = False
    is_adv_quest: bool = False
    is_adv_socialize: bool = False
    is_adv_story: bool = False
    is_adv_template: bool = False

    def __post_init__(self):
        convert_data = (
            (self.is_creature, "CREATURE"),
            (self.is_tribe_creature, "TRIBE_CREATURE"),
            (self.is_civ_creature, "CIV_CREATURE"),
            (self.is_space_creature, "SPACE_CREATURE"),
            (self.is_adventure_creature, "ADVENTURE_CREATURE"),
            (self.is_city_hall, "CITY_HALL"),
            (self.is_house, "HOUSE"),
            (self.is_industry, "INDUSTRY"),
            (self.is_entertainment, "ENTERTAINMENT"),
            (self.is_ufo, "UFO"),
            (self.is_adv_attack, "ADV_ATTACK"),
            (self.is_adv_collect, "ADV_COLLECT"),
            (self.is_adv_defend, "ADV_DEFEND"),
            (self.is_adv_explore, "ADV_EXPLORE"),
            (self.is_adv_explore, "ADV_EXPLORE"),
            (self.is_adv_unset, "ADV_UNSET"),
            (self.is_adv_puzzle, "ADV_PUZZLE"),
            (self.is_adv_quest, "ADV_QUEST"),
            (self.is_adv_socialize, "ADV_SOCIALIZE"),
            (self.is_adv_story, "ADV_STORY"),
            (self.is_adv_template, "ADV_TEMPLATE"),
        )
        self._params = tuple(
            value
            for key, value in convert_data
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class ModelsSearchParam(ABCSearchParam):
    is_land: bool = False
    is_air: bool = False
    is_water: bool = False

    def __post_init__(self):
        convert_data = (
            (self.is_land, "LAND"),
            (self.is_air, "AIR"),
            (self.is_water, "WATER"),
        )
        self._params = tuple(
            value
            for key, value in convert_data
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class PurposesSearchParam(ABCSearchParam):
    is_military: bool = False
    is_economic: bool = False
    is_cultural: bool = False
    is_colony: bool = False

    def __post_init__(self):
        convert_data = (
            (self.is_military, "MILITARY"),
            (self.is_economic, "ECONOMIC"),
            (self.is_cultural, "CULTURAL"),
            (self.is_colony, "COLONY"),
        )
        self._params = tuple(
            value
            for key, value in convert_data
            if key
        )

    def compose_string(self) -> str:
        return f"[{','.join(self._params)}]"


@dataclass
class SearchParams():
    fields: Optional[FieldsSearchParam] = None
    functions: Optional[FunctionsSearchParam] = None
    models: Optional[ModelsSearchParam] = None
    purposes: Optional[PurposesSearchParam] = None

    def __post_init__(self):
        self._fields = (
            self.fields
            if self.fields is not None else
            FieldsSearchParam()
        )
        self._functions = (
            self.functions
            if self.functions is not None else
            FunctionsSearchParam()
        )
        self._models = (
            self.models
            if self.models is not None else
            ModelsSearchParam()
        )
        self._purposes = (
            self.purposes
            if self.purposes is not None else
            PurposesSearchParam()
        )
