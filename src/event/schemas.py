from pydantic import BaseModel


class WeatherSchema(BaseModel):
    """Модель входящих данных от API."""
    temp: int
    humidity: int
