from typing import TYPE_CHECKING, Optional, Type, TypeVar

from .api import APIClient, SearchParams


if TYPE_CHECKING:
    from types import TracebackType

    from aiohttp import ClientSession

    from .enums import SearchFilter
    from .models import SearchServiceResult


class SporepediaClient():
    SporepediaClientType = TypeVar("SporepediaClientType", bound="SporepediaClient")

    def __init__(self):
        self._api = APIClient()

    async def search(
        self,
        text: str,
        lenght: int = 20,
        params: SearchParams = SearchParams(),
        filter: Optional["SearchFilter"] = None,
    ) -> "SearchServiceResult":
        result = await self._api.search(
            text=text,
            lenght=lenght,
            params=params,
            filter=filter
        )
        return result

    async def create(self, session: Optional["ClientSession"] = None) -> None:
        await self._api.create(session)

    async def close(self) -> None:
        await self._api.close()

    async def __aenter__(
        self: "SporepediaClient",
        session: Optional["ClientSession"] = None
    ) -> "SporepediaClient":
        await self.create(session)
        return self

    async def __aexit__(
        self,
        _exception_type: Type[BaseException],
        _exception: BaseException,
        _traceback: "TracebackType",
    ) -> None:
        await self.close()
