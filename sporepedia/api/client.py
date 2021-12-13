from typing import Any, Optional, Type, TypeVar
from types import TracebackType

import aiohttp

from sporepedia.api.methods import (
    SearchMixin,
)


class APIClient(SearchMixin):
    """
    Low level api
    """
    APIClientType = TypeVar("APIClientType", bound="APIClient")

    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> aiohttp.ClientResponse:
        if self._session is None:
            raise ValueError("Session is not exist")

        response = await self._session.request(
            url=url,
            method=method,
            **kwargs,
        )
        response.raise_for_status()
        return response

    async def create(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self._session = (
            aiohttp.ClientSession()
            if session is None else
            session
        )

    async def close(self) -> None:
        if self._session is None:
            raise ValueError("The session does not exist")

        await self._session.close()

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
