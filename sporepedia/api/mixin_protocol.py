from typing import TYPE_CHECKING, Protocol

from aiohttp import ClientResponse


class APIClientProtocol(Protocol):
    async def request(
        self,
        method: str,
        url: str,
        *args, **kw,
    ) -> ClientResponse:
        ...


# TODO: Maybe to `methods`
