from event.schemas import WeatherSchema
from infrastructure.gateways.api.api_constants import (
    WEATHER_API_KEY,
    WEATHER_API_TOKEN,
    WEATHER_API_URL,
)
from infrastructure.gateways.api.base_async_client import BaseAsyncClient


class WeatherAsyncClient(BaseAsyncClient):
    """Клиент для работы с API погоды."""

    def __init__(self):
        headers = {WEATHER_API_KEY: WEATHER_API_TOKEN}
        super().__init__(headers=headers)

    async def get_weather(self, lat: float, lon: float, url: str = WEATHER_API_URL) -> WeatherSchema:
        """Получение прогноза погоды."""
        weather = await self.get(url, params=dict(lat=lat, lon=lon))
        return WeatherSchema(**weather)


weather_async_client = WeatherAsyncClient()
