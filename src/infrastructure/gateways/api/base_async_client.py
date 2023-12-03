from httpx import AsyncClient, HTTPError
from httpx._status_codes import code as status_code

from infrastructure.gateways.api import error_constants, exceptions


class BaseAsyncClient:
    """Базовый асинхронный клиент для выполнения HTTP-запросов."""

    def __init__(self, headers: dict | None = None):
        self.async_client = AsyncClient()
        self.headers = headers

    async def get(self, url: str, params: dict | None = None) -> dict:
        """Выполняет асинхронный GET-запрос по указанному URL."""
        request_params = dict(
            url=url,
            headers=self.headers,
            params=params,
        )
        try:
            response = await self.async_client.get(url=url, headers=self.headers, params=params)
        except HTTPError as error:
            raise ConnectionError(error_constants.API_NOT_AVALIABLE.format(**request_params, error=error))
        response_status_code = response.status_code
        if response_status_code != status_code.OK:
            raise exceptions.StatusCodeNotOKError(
                error_constants.STATUS_CODE_ERROR.format(**request_params, status_code=response_status_code)
            )
        return response.json()
