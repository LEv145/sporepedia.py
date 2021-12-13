from typing import Any, Protocol

from aiohttp import ClientResponse


class APIClientProtocol(Protocol):
    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        """Protocol for api client"""
        ...


# TODO: Maybe to `methods`
