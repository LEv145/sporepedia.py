from types import TracebackType
from typing import Optional, Type, TypeVar

import aiohttp

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

    async def __aenter__(
        self: "APIClientType",
        session: Optional[aiohttp.ClientSession] = None
    ) -> "APIClientType":
        await self.create(session)
        return self

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

